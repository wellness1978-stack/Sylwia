// Renderuje ofertę do PDF (A4) w dwóch wersjach: PL (index.html) i EN (index.en.html).
// Użycie: node oferty/claude-w-praktyce/build.js [katalog_podgladow]
//
// Dane kontaktowe NIE są w repo (repo jest publiczne). Trzymaj je w
// kontakt.local.json obok tego skryptu (plik jest w .gitignore):
//   { "tekst": "Skontaktuj się z ...", "tekst_en": "Contact ...", "telefon": "+48 ..." }
// Bez tego pliku sekcja kontaktu jest pomijana.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const VERSIONS = [
  { lang: 'pl', src: 'index.html', out: 'Program-szkolenia-Claude-w-praktyce-biznesowej.pdf', textKey: 'tekst' },
  { lang: 'en', src: 'index.en.html', out: 'Training-program-Claude-in-business-practice.pdf', textKey: 'tekst_en' },
];

(async () => {
  const dir = __dirname;
  const previews = process.argv[2];
  const kontaktPath = path.join(dir, 'kontakt.local.json');
  const k = fs.existsSync(kontaktPath) ? JSON.parse(fs.readFileSync(kontaktPath, 'utf8')) : null;
  if (!k) console.warn('Brak kontakt.local.json: PDF-y bez sekcji kontaktu.');

  const browser = await chromium.launch();
  for (const v of VERSIONS) {
    let html = fs.readFileSync(path.join(dir, v.src), 'utf8');
    if (k && k[v.textKey]) {
      html = html
        .replaceAll('{{KONTAKT_TEKST}}', k[v.textKey])
        .replaceAll('{{TELEFON}}', k.telefon)
        .replaceAll('{{TELEFON_HREF}}', k.telefon.replace(/[^+\d]/g, ''));
    } else {
      html = html.replace(/<div class="contact">[\s\S]*?<\/div>/, '');
    }
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(dir, v.out), format: 'A4', printBackground: true, preferCSSPageSize: true });
    if (previews) {
      const pages = await page.$$('.page');
      for (let i = 0; i < pages.length; i++) {
        await pages[i].screenshot({ path: path.join(previews, `${v.lang}-p${i + 1}.png`) });
      }
    }
    await page.close();
  }
  await browser.close();
})();
