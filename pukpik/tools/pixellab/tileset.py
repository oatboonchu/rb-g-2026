# usage: tileset.py name "lower" "upper" outdir  -> saves outdir/name.json (16 tiles with corners + base64)
import json,sys,os,time,urllib.request
name,lower,upper,out=sys.argv[1:5]
H={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'}
def call(url,body=None):
  for w in (3,6,12,24,48,0):
    try:
      req=urllib.request.Request(url,data=json.dumps(body).encode() if body else None,headers=H,method='POST' if body else 'GET')
      return json.load(urllib.request.urlopen(req,timeout=120))
    except urllib.error.HTTPError as e:
      if e.code in (423,429,500,502,503) and w: time.sleep(w); continue
      print(name,'HTTP',e.code,e.read()[:300]); raise
    except Exception as e:
      if w: time.sleep(w); continue
      raise
os.makedirs(out,exist_ok=True)
if os.path.exists(f'{out}/{name}.json'): print(name,'skip'); sys.exit()
tid=os.environ.get('TID')
r={'tileset_id':tid} if tid else call('https://api.pixellab.ai/v2/create-tileset',{"lower_description":lower,"upper_description":upper,"tile_size":{"width":32,"height":32},**({"mode":os.environ["MODE"]} if os.environ.get("MODE") else {}),"transition_size":float(os.environ.get("TS","0")),**({"color_image":{"type":"base64","base64":__import__("base64").b64encode(open(os.environ["PAL"],"rb").read()).decode()}} if os.environ.get("PAL") else {}),"view":"high top-down","outline":"lineless","shading":"medium shading","detail":os.environ.get("DETAIL","medium detail"),"seed":2026})
tid=tid or r.get('tileset_id') or (r.get('data') or {}).get('id') or r.get('id')
job=r.get('background_job_id') or (r.get('data') or {}).get('background_job_id')
print(name,'started',json.dumps(r)[:200],flush=True)
for _ in range(120):
  time.sleep(5)
  try: g=json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.pixellab.ai/v2/tilesets/{tid}',headers=H),timeout=120))
  except urllib.error.HTTPError as e:
    if e.code==423: continue
    raise
  except Exception: continue
  st=g.get('status') or (g.get('data') or {}).get('status')
  if st in ('completed','complete','done','succeeded') or 'tiles' in json.dumps(g)[:5000] and st not in ('processing','pending','queued'):
    json.dump(g,open(f'{out}/{name}.json','w')); print(name,'done',st); break
else: print(name,'TIMEOUT')
