# usage: python3 batch.py jobs.tsv outdir size [view] [direction]   (tsv: name<TAB>description) — 3 at a time, retries on 429/network
import json,base64,sys,os,urllib.request,time,concurrent.futures as cf
jobs=[l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip()]
out,size=sys.argv[2],int(sys.argv[3]); view=sys.argv[4] if len(sys.argv)>4 else 'side'; dirn=sys.argv[5] if len(sys.argv)>5 else None
suffix=os.environ.get('SUFFIX',', game UI icon, centered, cute chunky pixel art')
os.makedirs(out,exist_ok=True)
def run(j):
  name,desc=j
  if os.path.exists(f'{out}/{name}.png'): return name+' skip'
  body={"description":desc+suffix,"image_size":{"width":size,"height":size},"no_background":True,"outline":os.environ.get("OUTLINE","single color black outline"),"shading":os.environ.get("SHADING","basic shading"),"detail":os.environ.get("DETAIL","medium detail"),"view":view,"seed":int(os.environ.get("SEED","2026"))}
  if dirn: body["direction"]=dirn
  if os.environ.get("PAL"): body["color_image"]={"type":"base64","base64":base64.b64encode(open(os.environ["PAL"],"rb").read()).decode()}
  for w in (3,6,12,24,48,0):
    try:
      req=urllib.request.Request('https://api.pixellab.ai/v1/generate-image-pixflux',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'})
      r=json.load(urllib.request.urlopen(req,timeout=180)); break
    except Exception as e:
      if not w: return name+' FAILED '+str(e)
      time.sleep(w)
  open(f'{out}/{name}.png','wb').write(base64.b64decode(r['image']['base64'])); return name+' ok'
with cf.ThreadPoolExecutor(3) as ex:
  for r in ex.map(run,jobs): print(r,flush=True)
