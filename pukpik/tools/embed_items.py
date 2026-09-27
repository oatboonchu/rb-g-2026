# Fills `const IT_ART = {...};` in index.html from sprites/items/<group>_<key>.png for the non-equipment items
# (rune_, food_, stone_, acc_, uq_, egg_). Safe to re-run.
import base64, glob, os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
du = lambda f: 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
fs = sorted(f for g in ('rune', 'food', 'stone', 'acc', 'uq', 'egg') for f in glob.glob(f'{root}/sprites/items/{g}_*.png'))
body = ',\n'.join(f"  {os.path.basename(f)[:-4]}: '{du(f)}'" for f in fs)
p = f'{root}/index.html'; s = open(p, encoding='utf-8').read()
s, k = re.subn(r"const IT_ART = \{.*?\};\n", lambda m: 'const IT_ART = {\n' + body + '\n};\n', s, count=1, flags=re.S)
assert k == 1
open(p, 'w', encoding='utf-8').write(s); print('item icons embedded:', len(fs))
