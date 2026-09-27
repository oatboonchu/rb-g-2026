# Builds pukpik/dressup.html: a dress-up preview of the layered m12 character (blank body + hair + eyes + brows).
# Layers are worked out in the page: each part image minus the bald body it was inpainted on.
import base64, json, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here); S = f'{root}/sprites'
du = lambda f: 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
art = {
  'blank': du(f'{S}/dressup3/blank.png'),
  'hair': {k: du(f'{S}/dressup3/hair_{k}.png') for k in ('emo', 'spiky', 'short', 'pony', 'bob', 'wolf')},
  'eye': {k: du(f'{S}/dressup3/eye_{k}.png') for k in ('sparkle', 'sharp', 'sleepy', 'cat', 'happy', 'fierce')},
  'm12hair': [du(f'{S}/style_trial/bases/m12.png')] + [du(f'{S}/style_trial/m12_hair/h{i:02d}.png') for i in range(1, 9)] + [du(f'{S}/style_trial/m12_hair/b{i:02d}.png') for i in range(1, 7)],
  'bases': [du(f'{S}/style_trial/bases/m{i:02d}.png') for i in range(1, 13)],
  'looks': [du(f'{S}/style_trial/{n}.png') for n in ('hero_s11_hero_a', 'hero_s42_hero_a', 'hero_s11_hero_b', 'hero_s42_hero_b')],
}
page = open(f'{here}/dressup_template.html', encoding='utf-8').read().replace('/*ART*/null', json.dumps(art))
open(f'{root}/dressup.html', 'w', encoding='utf-8').write(page); print('dressup.html', len(page))
