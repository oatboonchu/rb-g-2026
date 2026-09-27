# Fills `const FORM_ART = {...};` in index.html from sprites/forms/form_<colour>_<form>.png and, when all 12 frames
# exist, sprites/anim/f_<colour>_<form>_<idle|walk|attack>_<0-3>.png, plus extra facings in `dirs`. Safe to re-run.
import base64, os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
du = lambda f: 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
C = ['red', 'blue', 'yellow', 'brown', 'green']; F = ['atk', 'def', 'spd', 'hp', 'luk', 'rainbow', 'shadow', 'unique']
parts = []; n_anim = 0
for c in C:
    fs = []
    for f in F:
        png = f'{root}/sprites/forms/form_{c}_{f}.png'
        if not os.path.exists(png): continue
        frames = {a: [f'{root}/sprites/anim/f_{c}_{f}_{a}_{i}.png' for i in range(4)] for a in ('idle', 'walk', 'attack')}
        anim = ''
        if all(os.path.exists(x) for v in frames.values() for x in v):
            anim = ', anim: { ' + ', '.join(f"{a}: [{', '.join(repr(du(x)) for x in v)}]" for a, v in frames.items()) + ' }'; n_anim += 1
        # extra facings (e = east, ne = north-east, n = north): sprites/forms/dir/form_<c>_<f>_<d>.png + anim/f_<c>_<f>_<d>_<act>_<i>.png
        dirs = []
        for d in ('e', 'ne', 'n'):
            dp = f'{root}/sprites/forms/dir/form_{c}_{f}_{d}.png'
            dfr = {a: [f'{root}/sprites/anim/f_{c}_{f}_{d}_{a}_{i}.png' for i in range(4)] for a in ('idle', 'walk', 'attack')}
            if os.path.exists(dp) and all(os.path.exists(x) for v in dfr.values() for x in v):
                dirs.append(f"{d}: {{ png: '{du(dp)}', anim: {{ " + ', '.join(f"{a}: [{', '.join(repr(du(x)) for x in v)}]" for a, v in dfr.items()) + ' } }')
        if dirs: anim += ', dirs: { ' + ', '.join(dirs) + ' }'
        fs.append(f"{f}: {{ png: '{du(png)}'{anim} }}")
    parts.append(f"  {c}: {{ {', '.join(fs)} }}")
p = f'{root}/index.html'; s = open(p).read()
s, k = re.subn(r"const FORM_ART = \{.*?\};\n", lambda m: 'const FORM_ART = {\n' + ',\n'.join(parts) + '\n};\n', s, count=1, flags=re.S)
assert k == 1
open(p, 'w').write(s); print('forms embedded, with animation:', n_anim)
