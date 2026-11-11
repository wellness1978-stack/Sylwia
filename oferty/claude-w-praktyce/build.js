// Renderuje index.html do PDF (A4) i opcjonalnie podglądów PNG.
// Użycie: node oferty/claude-w-praktyce/build.js [katalog_podgladow]
//
// Dane kontaktowe NIE są w repo (repo jest publiczne). Trzymaj je w
// kontakt.local.json obok tego skryptu (plik jest w .gitignore):
//   { "tekst": "Skontaktuj się z ...", "telefon": "+48 ..." }
// Bez tego pliku sekcja kontaktu jest pomijana.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = __dirname;
  const previews = process.argv[2];
  let html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');

  const kontaktPath = path.join(dir, 'kontakt.local.json');
  if (fs.existsSync(kontaktPath)) {
    const k = JSON.parse(fs.readFileSync(kontaktPath, 'utf8'));
    html = html
      .replaceAll('{{KONTAKT_TEKST}}', k.tekst)
      .replaceAll('{{TELEFON}}', k.telefon)
      .replaceAll('{{TELEFON_HREF}}', k.telefon.replace(/[^+\d]/g, ''));
  } else {
    console.warn('Brak kontakt.local.json: PDF bez sekcji kontaktu.');
    html = html.replace(/<div class="contact">[\s\S]*?<\/div>/, '');
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(dir, 'Program-szkolenia-Claude-w-praktyce-biznesowej.pdf'),
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
  });
  if (previews) {
    const pages = await page.$$('.page');
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(previews, `p${i + 1}.png`) });
    }
  }
  await browser.close();
})();
