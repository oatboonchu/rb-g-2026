// node mask.js grow  -> nw/mask_<d>.png (white = sword area) and nw/prev_masks.png
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const grow = +process.argv[2] || 2; const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 300 } });
  const dirs = ['s', 'e', 'ne', 'n'];
  const srcs = Object.fromEntries(dirs.map(d => [d, 'data:image/png;base64,' + fs.readFileSync(`nw/src_${d}.png`).toString('base64')]));
  const out = await p.evaluate(async ({ srcs, grow }) => {
    const res = {}; const prev = document.createElement('canvas'); prev.width = 1024; prev.height = 256; const pg = prev.getContext('2d'); pg.imageSmoothingEnabled = false;
    let x0 = 0;
    for (const [d, src] of Object.entries(srcs)) {
      const im = new Image(); im.src = src; await im.decode();
      const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); g.drawImage(im, 0, 0);
      const px = g.getImageData(0, 0, 64, 64).data, m = new Uint8Array(4096);
      for (let i = 0; i < 4096; i++) { const r = px[i*4], gg = px[i*4+1], bb = px[i*4+2], a = px[i*4+3]; if (a < 128) continue;
        const mx = Math.max(r, gg, bb), mn = Math.min(r, gg, bb), sat = mx ? (mx - mn) / mx : 0;
        if (mx > 150 && sat < .18) m[i] = 1; }
      // keep only big connected blobs (the blade), drop eye highlights
      const lab = new Int32Array(4096).fill(-1), sizes = [];
      for (let i = 0; i < 4096; i++) if (m[i] && lab[i] < 0) { const st = [i]; lab[i] = sizes.length; let n = 0; while (st.length) { const j = st.pop(); n++; const x = j % 64, y = j / 64 | 0; for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]) { const X = x+dx, Y = y+dy; if (X<0||Y<0||X>63||Y>63) continue; const k = Y*64+X; if (m[k] && lab[k] < 0) { lab[k] = sizes.length; st.push(k); } } } sizes.push(n); }
      let mm = new Uint8Array(4096); for (let i = 0; i < 4096; i++) if (lab[i] >= 0 && sizes[lab[i]] >= 12) mm[i] = 1;
      for (let k = 0; k < grow; k++) { const n2 = mm.slice(); for (let i = 0; i < 4096; i++) if (mm[i]) { const x = i % 64, y = i / 64 | 0; for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1]]) { const X = x+dx, Y = y+dy; if (X>=0&&Y>=0&&X<64&&Y<64) n2[Y*64+X] = 1; } } mm = n2; }
      const mc = document.createElement('canvas'); mc.width = mc.height = 64; const mg = mc.getContext('2d'); const id = mg.createImageData(64, 64);
      for (let i = 0; i < 4096; i++) { const v = mm[i] ? 255 : 0; id.data.set([v, v, v, 255], i * 4); } mg.putImageData(id, 0, 0);
      res[d] = mc.toDataURL();
      pg.drawImage(c, x0, 0, 256, 256); pg.globalAlpha = .5; pg.drawImage(mc, x0, 0, 256, 256); pg.globalAlpha = 1; x0 += 256;
    }
    res.prev = prev.toDataURL(); return res; }, { srcs, grow });
  for (const [k, v] of Object.entries(out)) fs.writeFileSync(k === 'prev' ? 'nw/prev_masks.png' : `nw/mask_${k}.png`, Buffer.from(v.split(',')[1], 'base64'));
  await b.close(); })();
