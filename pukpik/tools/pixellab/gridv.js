// node gridv.js in.png out.png  -> 10x zoom with a grid every 8px and coordinates
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [inp, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 700, height: 700 } });
  const src = 'data:image/png;base64,' + fs.readFileSync(inp).toString('base64');
  const d = await p.evaluate(async src => { const im = new Image(); im.src = src; await im.decode(); const S = 10, c = document.createElement('canvas'); c.width = c.height = 64 * S + 30; const g = c.getContext('2d');
    g.fillStyle = '#556'; g.fillRect(0, 0, c.width, c.height); g.imageSmoothingEnabled = false; g.drawImage(im, 30, 30, 64 * S, 64 * S);
    g.strokeStyle = 'rgba(255,255,255,.25)'; g.fillStyle = '#fff'; g.font = '11px sans-serif';
    for (let i = 0; i <= 64; i += 4) { g.lineWidth = i % 8 ? .5 : 1.2; g.beginPath(); g.moveTo(30 + i * S, 30); g.lineTo(30 + i * S, 30 + 64 * S); g.moveTo(30, 30 + i * S); g.lineTo(30 + 64 * S, 30 + i * S); g.stroke(); if (i % 8 === 0) { g.fillText(i, 30 + i * S - 4, 20); g.fillText(i, 4, 30 + i * S + 4); } }
    return c.toDataURL(); }, src);
  fs.writeFileSync(out, Buffer.from(d.split(',')[1], 'base64')); await b.close(); })();
