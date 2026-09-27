# python3 inpaint.py src.png mask.png "desc" out.png   (env SEED, TG)
import json,base64,sys,os,urllib.request,time
src,mask,desc,out=sys.argv[1:5]
b64=lambda f:{"type":"base64","base64":base64.b64encode(open(f,'rb').read()).decode()}
body={"description":desc+", clean chunky pixel art, soft highlights, limited color palette","image_size":{"width":64,"height":64},"inpainting_image":b64(src),"mask_image":b64(mask),
 "no_background":True,"outline":"selective outline","shading":"basic shading","detail":"medium detail","text_guidance_scale":float(os.environ.get("TG","6")),"seed":int(os.environ.get("SEED","2026"))}
if os.environ.get("PAL"): body["color_image"]=b64(os.environ["PAL"])
for w in (3,6,12,24,48,0):
  try:
    req=urllib.request.Request('https://api.pixellab.ai/v1/inpaint',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'})
    r=json.load(urllib.request.urlopen(req,timeout=240)); break
  except Exception as e:
    print('retry',e)
    if not w: raise
    time.sleep(w)
open(out,'wb').write(base64.b64decode(r['image']['base64'])); print(out,r.get('usage'))
