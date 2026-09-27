// node pmask.js name "x0,y0,x1,y1;..." [minus "x0,y0,x1,y1;..."] -> pd/mask_<name>.png (white = repaint; rects inclusive)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [name, add, sub] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
  const d = await p.evaluate(([add, sub]) => { const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, 64, 64);
    const R = (s, col) => (s || '').split(';').filter(Boolean).forEach(r => { const [a, b2, x, y] = r.split(',').map(Number); g.fillStyle = col; g.fillRect(a, b2, x - a + 1, y - b2 + 1); });
    R(add, '#fff'); R(sub, '#000'); return c.toDataURL(); }, [add, sub]);
  fs.writeFileSync((process.env.MD||'pd')+`/mask_${name}.png`, Buffer.from(d.split(',')[1], 'base64')); await b.close(); })();
