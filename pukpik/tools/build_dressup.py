# Builds pukpik/dressup.html: a dress-up preview of the layered character (body + outfit + hair + hat + weapon).
# Layers are worked out in the page: each part image minus the bald body it was inpainted on.
import base64, json, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); S = f'{root}/sprites'
du = lambda f: 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
art = {
  'bald': du(f'{S}/dressup/bald.png'), 'bald12': du(f'{S}/dressup/bald_dn12.png'),
  'hair': {k: du(f'{S}/dressup/hair_{k}.png') for k in ('spiky', 'pony', 'blond')},
  'hat': {k: du(f'{S}/dressup/hat_{k}_dn12.png') for k in ('wizard', 'helm')},
  'outfit': {k: du(f'{S}/dressup/out_{k}.png') for k in ('ranger', 'knight')},
  'weapon': [du(f'{S}/items/weapon_{i}.png') for i in range(10)],
  'looks': [du(f'{S}/style_trial/{n}.png') for n in ('hero_s11_hero_a', 'hero_s42_hero_a', 'hero_s11_hero_b', 'hero_s42_hero_b')],
}
page = open(f'{here}/dressup_template.html', encoding='utf-8').read().replace('/*ART*/null', json.dumps(art))
open(f'{root}/dressup.html', 'w', encoding='utf-8').write(page); print('dressup.html', len(page))
