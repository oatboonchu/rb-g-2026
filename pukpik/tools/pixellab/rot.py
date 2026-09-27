import json,base64,sys,os,urllib.request,time
src,todir,out=sys.argv[1:4]
img=base64.b64encode(open(src,'rb').read()).decode()
body={"image_size":{"width":64,"height":64},"from_image":{"type":"base64","base64":img},"from_direction":"south","to_direction":todir,
 "from_view":"low top-down","to_view":"low top-down","image_guidance_scale":float(os.environ.get("IG","3"))}
for k in range(5):
  try:
    req=urllib.request.Request('https://api.pixellab.ai/v1/rotate',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'})
    r=json.load(urllib.request.urlopen(req,timeout=300)); break
  except Exception as e:
    print('retry',e); time.sleep(2**k*3)
open(out,'wb').write(base64.b64decode(r['image']['base64'])); print(todir,r.get('usage'))
