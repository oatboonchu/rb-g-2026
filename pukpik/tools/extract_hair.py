# Cuts the hair out of m12 hairstyle images (PixelLab /inpaint on m12c with mask_b) into dress-up layers.
# python3 pukpik/tools/extract_hair.py  -> pukpik/sprites/dressup3/hair12/<name>.png
# Layer = pixels that differ from the bald body (dressup3/blank.png), minus the face: the page draws its own eyes and brows.
# Magenta (255,0,255) marks bald scalp the new hair leaves uncovered; the page erases the body there.
import os
from collections import Counter
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__)); S = f'{os.path.dirname(here)}/sprites'
NAMES = [f'a{i:02d}' for i in range(1, 9)] + [f'b{i:02d}' for i in range(1, 7)]
B = Image.open(f'{S}/dressup3/blank.png').convert('RGBA').load()
SKIN = {(255, 241, 176), (242, 194, 156), (245, 154, 154), (201, 138, 100), (138, 90, 68)}
EYE_X = 23
face = lambda x, y: B[x, y][3] > 100 and B[x, y][:3] in SKIN
os.makedirs(f'{S}/dressup3/hair12', exist_ok=True)
for n in NAMES:
  P = Image.open(f'{S}/style_trial/m12_hair/{n}.png').convert('RGBA').load()
  keep = [[P[x, y][3] >= 100 and sum(abs(P[x, y][i] - B[x, y][i]) for i in range(4)) > 36 for x in range(64)] for y in range(64)]
  # the hair's own colours, taken above the face (brown hair and clips share shades with the skin)
  pal = Counter(P[x, y][:3] for y in range(17) for x in range(64) if keep[y][x])
  pal = {c for c, k in pal.items() if k >= 3}
  # other skin shades are the face under the fringe, not hair (the page would tint them into hair-coloured blobs)
  for y in range(64):
    for x in range(64):
      if keep[y][x] and P[x, y][:3] in SKIN and P[x, y][:3] not in pal: keep[y][x] = False
  # the page's eyes cover x 23-43 in rows 21-27, so nothing survives on the face there; rows 17-20 keep only bang tips hanging from the hair above.
  # Left of the eyes (x <= 22) side locks may lie over the cheek, or they float apart from the head.
  for y in range(17, 40):
    for x in range(64):
      if keep[y][x] and face(x, y) and (y >= 21 or not keep[y - 1][x]) and not (21 <= y <= 30 and x <= EYE_X - 1 and P[x, y][:3] in pal): keep[y][x] = False
  # below the chin only hair past the shoulders (where the body is empty) counts, not shirt, collar or hand changes
  for y in range(31, 64):
    for x in range(64):
      if keep[y][x] and ((B[x, y][3] > 100 and not face(x, y)) or P[x, y][:3] not in pal): keep[y][x] = False
  # drop loose bits of under 8 pixels
  seen = set()
  for y in range(64):
    for x in range(64):
      if keep[y][x] and (x, y) not in seen:
        comp = [(x, y)]; seen.add((x, y)); i = 0
        while i < len(comp):
          cx, cy = comp[i]; i += 1
          for a in (-1, 0, 1):
            for b in (-1, 0, 1):
              nx, ny = cx + a, cy + b
              if 0 <= nx < 64 and 0 <= ny < 64 and keep[ny][nx] and (nx, ny) not in seen: seen.add((nx, ny)); comp.append((nx, ny))
        if len(comp) < 8:
          for cx, cy in comp: keep[cy][cx] = False
  o = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); O = o.load()
  for y in range(64):
    for x in range(64):
      if keep[y][x]: O[x, y] = P[x, y]
      elif y < 20 and P[x, y][3] < 100 and B[x, y][3] > 100: O[x, y] = (255, 0, 255, 255)
  o.save(f'{S}/dressup3/hair12/{n}.png')
print('hair12', len(NAMES))
