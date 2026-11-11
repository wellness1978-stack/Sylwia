# LinkedIn Style Cloner

Podajesz link do profilu LinkedIn. Claude pobiera posty tej osoby, analizuje jej styl (hooki, strukturę, rytm, emoji, słownictwo, grafiki) i tworzy **osobny skill**, którym piszesz własne posty w podobnym stylu, po polsku i po angielsku.

Jeden profil = jeden skill (`.claude/skills/<nazwa>-voice/`).

## Jak to działa

```
link do profilu
   → fetch_posts.py   pobiera ~60 postów przez Apify (bez logowania na Twoje konto)
   → stats.py         twarde metryki: długość, hooki, emoji, hashtagi, top vs słabe posty
   → analiza Claude   reguły stylu z dowodami (liczby + cytaty)
   → nowy skill       .claude/skills/<nazwa>-voice/ + 2 posty testowe
```

## Konfiguracja (raz)

1. Załóż konto na [apify.com](https://apify.com). Darmowy plan ma miesięczny kredyt, a pobranie 60 postów kosztuje ok. 10–15 centów (przy cenach ~1,5–2 USD za 1000 postów; sprawdź aktualną cenę na stronie aktora).
2. Skopiuj token: Settings → API & Integrations.
3. W katalogu repo:
   ```bash
   cp .env.example .env
   ```
   Wpisz token do `.env`, a potem:
   ```bash
   set -a; source .env; set +a
   ```
4. Uruchom Claude Code w katalogu repo:
   ```bash
   claude
   ```

## Użycie

Utworzenie skilla:

```
/linkedin-style-cloner https://www.linkedin.com/in/ktos/
```

albo po prostu: „zrób skill ze stylu tego profilu: https://www.linkedin.com/in/ktos/”.

Pisanie postów (po utworzeniu skilla):

```
napisz post w stylu Ktoś o tym, że <Twój temat / notatka / historia>
write a LinkedIn post in Ktoś's style about <topic>
```

## Gdy coś nie działa

- **Brak tokenu:** skrypt powie, co zrobić.
- **Aktor zmienił format danych:** surowa odpowiedź jest w `data/<nazwa>/raw.json`. Claude dopasuje mapowanie pól i przetworzy ją ponownie bez płacenia drugi raz (`--from-raw`).
- **Aktor przestał działać:** w Apify Store jest kilka podobnych („LinkedIn profile posts no cookies”). Podmień przez `APIFY_ACTOR=autor~nazwa` w `.env`.
- **Bez Apify:** wklej 20–40 postów do `data/<nazwa>/manual.txt`, oddzielone linią `---`. Claude użyje trybu `--from-text`.

## Uwagi

- Aktor Apify pobiera publiczne posty z własnej infrastruktury, więc **Twoje konto LinkedIn nie bierze w tym udziału** i nie ryzykujesz jego blokady. Regulamin LinkedIna formalnie zabrania scrapowania, ale to ryzyko spoczywa na dostawcy usługi, a nie na Tobie jako użytkowniczce gotowych danych. Używaj do analizy na własny użytek.
- `data/` jest w `.gitignore`: surowe posty innych osób nie trafiają do repo.
- Skill przejmuje mechanikę stylu, a nie treść. Historie, fakty i opinie w postach muszą być Twoje.

## Struktura

```
.claude/skills/linkedin-style-cloner/
├── SKILL.md                         instrukcje „aplikacji”
├── scripts/fetch_posts.py           pobieranie + normalizacja (Python 3.8+, bez zależności)
├── scripts/stats.py                 metryki stylu
├── references/analysis-framework.md co analizujemy
└── templates/voice-skill-template.md szablon skilla wynikowego
```
