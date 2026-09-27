import json,base64,sys,os,urllib.request
color,action,desc,out=sys.argv[1:5]
ref=base64.b64encode(open(os.environ.get('REF') or f'slime_{color}.png','rb').read()).decode()
body={"description":desc,"action":action,"image_size":{"width":64,"height":64},"reference_image":{"type":"base64","base64":ref},
 "view":"low top-down","direction":os.environ.get("DIR","south"),"n_frames":4,"seed":int(os.environ.get("SEED","2026")),"image_guidance_scale":float(os.environ.get("IG","3")),"text_guidance_scale":float(os.environ.get("TG","6")),"inpainting_images":[{"type":"base64","base64":ref},None,None,None] if os.environ.get("LOCK") else [None]*4,"negative_description":"white arcs, motion lines, slash effects, weapon, extra limbs, background, shadow blur"}
req=urllib.request.Request('https://api.pixellab.ai/v1/animate-with-text',data=json.dumps(body).encode(),
 headers={'Authorization':'Bearer '+os.environ['PIXELLAB_API_KEY'],'Content-Type':'application/json'})
r=json.load(urllib.request.urlopen(req,timeout=300))
print(color,action,r.get('usage'))
for i,im in enumerate(r['images']): open(f'{out}_{i}.png','wb').write(base64.b64decode(im['base64']))
