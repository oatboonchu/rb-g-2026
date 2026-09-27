# usage: ui.py name "description" W H outdir [palette]
import json,sys,os,time,base64,urllib.request
name,desc,w,h,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]; pal=sys.argv[6] if len(sys.argv)>6 else None
H={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'}
os.makedirs(out,exist_ok=True)
if os.path.exists(f'{out}/{name}.png'): print(name,'skip'); sys.exit()
body={"description":desc,"image_size":{"width":w,"height":h},"no_background":True,"seed":2026}
if pal: body["color_palette"]=pal
for wt in (3,6,12,24,0):
  try: r=json.load(urllib.request.urlopen(urllib.request.Request('https://api.pixellab.ai/v2/generate-ui-v2',data=json.dumps(body).encode(),headers=H),timeout=120)); break
  except Exception as e:
    if not wt: raise
    time.sleep(wt)
job=r.get('background_job_id'); print(name,'job',job,flush=True)
for _ in range(120):
  time.sleep(5)
  try: g=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.pixellab.ai/v2/background-jobs/{job}',headers=H),timeout=60))
  except Exception: continue
  if g.get('status')=='completed':
    lr=g.get('last_response') or {}; ims=lr.get('images') or ([lr['image']] if lr.get('image') else [])
    if not ims: print(name,'no image', json.dumps(g)[:400]); break
    im=ims[0]; b=im.get('base64') or (im.get('image') or {}).get('base64')
    open(f'{out}/{name}.png','wb').write(base64.b64decode(b)); print(name,'done',len(ims),'images'); break
  if g.get('status') in ('failed','error'): print(name,'FAILED',json.dumps(g)[:300]); break
