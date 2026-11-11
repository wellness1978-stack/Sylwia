// Renderuje index.html do PDF (A4) i podglądów PNG.
// Użycie: node oferty/claude-w-praktyce/build.js [katalog_podgladow]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const dir = __dirname;
  const previews = process.argv[2];
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(dir, 'Program-szkolenia-Claude-w-praktyce-biznesowej.pdf'),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
  });
  if (previews) {
    await page.emulateMedia({ media: 'print' });
    const pages = await page.$$('.page');
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(previews, `p${i + 1}.png`) });
    }
  }
  await browser.close();
})();
