const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [out, dir, ...names] = process.argv.slice(2);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1100, height: 100 } });
  await pg.setContent(`<body style="margin:0;display:flex;flex-wrap:wrap;width:1100px;background:#E9DFC9;font:10px sans-serif">${names.map(n => `<div style="width:108px;text-align:center"><img src="data:image/png;base64,${fs.readFileSync(dir + '/' + n + '.png').toString('base64')}" style="width:96px;height:96px;image-rendering:pixelated"><br>${n}</div>`).join('')}</body>`);
  await pg.screenshot({ path: out, fullPage: true }); await b.close(); })();
