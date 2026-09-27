const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [out, ...files] = process.argv.slice(2);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1250, height: 100 } });
  await pg.setContent(`<body style="margin:0;display:flex;flex-wrap:wrap;background:#1E2029">${files.map(f => `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}" style="width:192px;height:192px;margin:8px;image-rendering:pixelated">`).join('')}</body>`);
  await pg.screenshot({ path: out, fullPage: true }); await b.close(); })();
