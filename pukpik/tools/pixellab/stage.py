# usage: stage.py color name "description" strength -> sprites/<name>.png using slime_<color>.png as the start image
import json,base64,sys,os,urllib.request,time
color,name,desc,strength=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
if os.path.exists(name+'.png'): print(name,'skip'); sys.exit()
ref=base64.b64encode(open(f'slime_{color}.png','rb').read()).decode()
body={"description":desc,"image_size":{"width":64,"height":64},"no_background":True,"outline":"single color black outline","shading":"basic shading","detail":"medium detail","view":"low top-down","direction":"south","seed":2026,"init_image":{"type":"base64","base64":ref},"init_image_strength":strength}
for w in (3,6,12,24,0):
  try:
    r=json.load(urllib.request.urlopen(urllib.request.Request('https://api.pixellab.ai/v1/generate-image-pixflux',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'}),timeout=180)); break
  except Exception as e:
    if not w: raise
    time.sleep(w)
open(name+'.png','wb').write(base64.b64decode(r['image']['base64'])); print(name,'ok')
