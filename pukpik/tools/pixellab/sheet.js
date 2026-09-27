// usage: node sheet.js out.png file1 file2 ... (renders side by side at 3x, on a checker bg)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const [out, ...files] = process.argv.slice(2);
  const imgs = files.map(f => 'data:image/png;base64,' + fs.readFileSync(f).toString('base64'));
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 200 * Math.min(files.length, 8), height: 200 * Math.ceil(files.length / 8) } });
  await pg.setContent(`<body style="margin:0;display:flex;flex-wrap:wrap;background:#9CD27E">${imgs.map(s => `<img src="${s}" style="width:192px;height:192px;margin:4px;image-rendering:pixelated;background:#A6DB88">`).join('')}</body>`);
  await pg.waitForTimeout(200); await pg.screenshot({ path: out, fullPage: true }); await b.close();
})();
