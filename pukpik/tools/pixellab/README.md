# สคริปต์ PixelLab ที่ใช้ทำภาพเกม

ทุกสคริปต์อ่านคีย์จากตัวแปร `PIXELLAB_API_KEY` ต้องตั้งก่อนใช้ (`export PIXELLAB_API_KEY=...`) ห้ามเขียนคีย์ลงไฟล์
สคริปต์ .js ใช้ Playwright (`npm i -g playwright` แล้วรันด้วย `NODE_PATH=$(npm root -g) node ...`)
รันจากโฟลเดอร์ที่จะเก็บภาพ เพราะสคริปต์อ่านและเขียนไฟล์ตาม path ที่ส่งไป

| สคริปต์ | ใช้ทำอะไร |
|---|---|
| `batch.py jobs.tsv outdir size [view] [direction]` | pixflux หลายภาพจากไฟล์ tsv (`ชื่อ<TAB>คำบรรยาย`) ทีละ 3 ภาพ มี retry · env: `SUFFIX` `SEED` `OUTLINE` `SHADING` `DETAIL` `PAL` (ไฟล์พาเลต) |
| `anim.py color action "desc" out` | animate-with-text 4 เฟรม · env: `REF` (ภาพต้นแบบ) `LOCK=1` (ล็อกเฟรมแรก) `IG` `TG` `DIR` `SEED` |
| `rot.py src.png direction out.png` | หมุนภาพหน้าตรงไปทิศอื่น (east, north-east, north ...) · env: `IG` |
| `inpaint.py src.png mask.png "desc" out.png` | วาดทับเฉพาะส่วนสีขาวใน mask · env: `SEED` `TG` `PAL` |
| `pmask.js name "x0,y0,x1,y1;..." ["ลบ..."]` | สร้าง mask 64×64 จากสี่เหลี่ยม (ขอบรวม) · env: `MD` โฟลเดอร์ที่เก็บ |
| `tileset.py`, `stage.py`, `ui.py` | ลายพื้น (v2 create-tileset), สไลม์ขั้นถัดไป, ชิ้น UI |
| `sheet.js`, `dsheet.js`, `isheet.js`, `gridv.js`, `mask.js` | ทำภาพรวมไว้ดูผล / ขยายดูพิกเซลพร้อมกริด / สร้าง mask ดาบอัตโนมัติ |

เครื่องมือที่เกี่ยวกับตัวเกมอยู่ที่ `pukpik/tools/` (embed_forms.py, embed_items.py, pngopt.py, build_dressup.py)
พาเลตสไตล์ใหม่: `pukpik/sprites/style_trial/palette_b.png`
