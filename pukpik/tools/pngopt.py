# Lossless PNG shrinker (pure Python): decode 8-bit RGB/RGBA PNGs, write palette PNGs (+tRNS) when <=256 colours,
# otherwise re-deflate RGBA at level 9 with per-row adaptive filters. Used on every data:image/png URL in a file.
import zlib,struct,base64,re,sys
def chunks(b):
    i=8
    while i<len(b):
        n=struct.unpack('>I',b[i:i+4])[0]; t=b[i+4:i+8]; yield t,b[i+8:i+8+n]; i+=12+n
def decode(b):
    ihdr=None; idat=b''; plte=None; trns=None
    for t,d in chunks(b):
        if t==b'IHDR': ihdr=struct.unpack('>IIBBBBB',d)
        elif t==b'IDAT': idat+=d
        elif t==b'PLTE': plte=d
        elif t==b'tRNS': trns=d
    w,h,depth,ct,_,_,il=ihdr
    if il!=0 or ct not in (2,6,3) or (depth!=8 and ct!=3): return None
    bpp={2:3,6:4,3:1}[ct]; raw=zlib.decompress(idat); stride=(w*depth+7)//8 if ct==3 else w*bpp; out=[]; prev=bytearray(stride); p=0
    for y in range(h):
        f=raw[p]; line=bytearray(raw[p+1:p+1+stride]); p+=1+stride
        for x in range(stride):
            a=line[x-bpp] if x>=bpp else 0; up=prev[x]; c=prev[x-bpp] if x>=bpp else 0
            if f==1: line[x]=(line[x]+a)&255
            elif f==2: line[x]=(line[x]+up)&255
            elif f==3: line[x]=(line[x]+((a+up)>>1))&255
            elif f==4:
                pa=abs(up-c); pb=abs(a-c); pc=abs(a+up-2*c)
                line[x]=(line[x]+(a if pa<=pb and pa<=pc else up if pb<=pc else c))&255
        out.append(bytes(line)); prev=line
    px=[]
    for line in out:
        for x in range(w):
            if ct==6: px.append(tuple(line[x*4:x*4+4]))
            elif ct==2: px.append(tuple(line[x*3:x*3+3])+(255,))
            else:
                i=(line[x*depth//8]>>(8-depth-(x*depth)%8))&((1<<depth)-1) if depth<8 else line[x]; r,g,bb=plte[i*3:i*3+3]; al=trns[i] if trns and i<len(trns) else 255; px.append((r,g,bb,al))
    return w,h,px
def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
def encode(w,h,px):
    px=[(0,0,0,0) if p[3]==0 else p for p in px]   # all fully transparent pixels become one colour
    cols=sorted(set(px),key=lambda c:(c[3]==255,c))
    if len(cols)<=256:
        idx={c:i for i,c in enumerate(cols)}; depth=8 if len(cols)>16 else 4 if len(cols)>4 else 2 if len(cols)>2 else 1
        per=8//depth; rows=b''
        for y in range(h):
            row=[idx[px[y*w+x]] for x in range(w)]; bs=bytearray()
            for x in range(0,w,per):
                v=0
                for k in range(per): v=(v<<depth)|(row[x+k] if x+k<w else 0)
                bs.append(v)
            rows+=b'\x00'+bytes(bs)
        plte=b''.join(bytes(c[:3]) for c in cols); ntr=sum(1 for c in cols if c[3]<255)
        out=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,depth,3,0,0,0))+chunk(b'PLTE',plte)
        if ntr: out+=chunk(b'tRNS',bytes(c[3] for c in cols[:ntr]))
        return out+chunk(b'IDAT',zlib.compress(rows,9))+chunk(b'IEND',b'')
    rows=b''.join(b'\x00'+bytes(v for x in range(w) for v in px[y*w+x]) for y in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(rows,9))+chunk(b'IEND',b'')
def shrink(b):
    try:
        d=decode(b)
        if not d: return b
        n=encode(*d); return n if len(n)<len(b) else b
    except Exception as e:
        print('skip',e,file=sys.stderr); return b
if __name__=='__main__':
    path=sys.argv[1]; s=open(path).read(); before=len(s); cache={}
    def sub(m):
        k=m.group(1)
        if k not in cache: cache[k]=base64.b64encode(shrink(base64.b64decode(k))).decode()
        return 'data:image/png;base64,'+cache[k]
    s=re.sub(r'data:image/png;base64,([A-Za-z0-9+/=]+)',sub,s)
    open(path,'w').write(s); print(f'{path}: {before:,} -> {len(s):,} bytes, {len(cache)} images')
