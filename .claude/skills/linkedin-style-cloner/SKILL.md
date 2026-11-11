---
name: linkedin-style-cloner
description: Analizuje posty z dowolnego profilu LinkedIn (na podstawie linku) i tworzy z nich nowy skill do pisania postów w tym stylu, po polsku i po angielsku. Używaj, gdy użytkowniczka prosi o "skill w stylu [osoby/link]", "przeanalizuj styl tego profilu LinkedIn", "sklonuj styl pisania", "zrób skill z postów tego autora" albo wkleja link linkedin.com/in/... z prośbą o styl.
---

# LinkedIn Style Cloner

Z linku do profilu LinkedIn tworzysz **jeden skill na jedną osobę**: `.claude/skills/<slug>-voice/`. Ten skill pisze nowe posty na tematy użytkowniczki, korzystając z mechaniki stylu autora (hooki, struktura, rytm, formatowanie, słownictwo), po polsku i po angielsku.

Polecenia uruchamiaj z katalogu głównego repo. Dane robocze trafiają do `data/<slug>/` (folder jest w `.gitignore`). Pliki `references/` i `templates/` wymienione niżej leżą w katalogu tego skilla.

## Krok 1: Zapytaj o link

Jeśli użytkowniczka nie podała linku, zapytaj tylko o to: „Podaj link do profilu LinkedIn (linkedin.com/in/...)”. Nie zadawaj innych pytań na start.

- `slug` = końcówka URL po `/in/`, małymi literami, bez znaków specjalnych (np. `linkedin.com/in/jan-kowalski-123/` → `jan-kowalski-123`).
- Jeśli `.claude/skills/<slug>-voice/` już istnieje, zapytaj, czy go odświeżyć (nadpisać), czy przerwać.

## Krok 2: Pobierz posty

```bash
python3 .claude/skills/linkedin-style-cloner/scripts/fetch_posts.py "<URL>" --out data/<slug> --max-posts 60
```

- Wymaga zmiennej `APIFY_TOKEN`. Jeśli jej brakuje, skrypt kończy się komunikatem. Wtedy wyjaśnij krótko: konto na apify.com → Settings → API & Integrations → skopiuj token → `export APIFY_TOKEN=...` (albo wpisz go do pliku `.env` w repo i uruchom `set -a; source .env; set +a`). Nigdy nie proś o wklejenie tokenu do czatu.
- Domyślny aktor to `harvestapi~linkedin-profile-posts` (bez logowania, bez cookies, więc konto użytkowniczki nie jest zagrożone). Inny aktor ustawisz flagą `--actor` lub zmienną `APIFY_ACTOR`. Dodatkowe pola wejścia aktora podasz przez `--extra-input '{"pole": wartość}'`.
- 60 postów wystarczy. Powyżej ~80 styl przestaje się zmieniać, rośnie tylko koszt.
- **Jeśli skrypt zgłosi „Brak postów z tekstem”**: otwórz `data/<slug>/raw.json`, sprawdź, pod jakimi kluczami jest tekst, data i reakcje, popraw listy ścieżek w funkcji `normalize()` w `fetch_posts.py` i uruchom ponownie z `--from-raw data/<slug>/raw.json` (bez ponownego płacenia za pobranie).
- **Plan awaryjny** (brak Apify, profil prywatny, aktor nie działa): poproś o wklejenie 20–40 postów do `data/<slug>/manual.txt`, oddzielonych linią `---`, i uruchom `--from-text data/<slug>/manual.txt`.
- Jeśli wyszło mniej niż 15 postów z tekstem, powiedz to wprost: profil stylu będzie mniej wiarygodny.

## Krok 3: Policz metryki

```bash
python3 .claude/skills/linkedin-style-cloner/scripts/stats.py data/<slug>/posts.json > data/<slug>/stats.md
```

## Krok 4: Przeczytaj wszystko

1. `data/<slug>/stats.md` w całości.
2. `data/<slug>/posts.md` w całości, każdy post. Nie streszczaj z próbki.
3. Grafiki z `data/<slug>/images/` (Read), żeby opisać warstwę wizualną: karuzele, zdjęcia, kolory, typografię, tekst na grafikach.

## Krok 5: Analiza

Przeanalizuj posty według `references/analysis-framework.md` i zapisz wynik w `data/<slug>/style-analysis.md`. Zasady:
- Każda reguła ma **dowód**: liczbę ze `stats.md` albo dosłowny cytat z postu (z id).
- Porównaj top 20% i najsłabsze 20% postów: co odróżnia posty, które działają? Te różnice to najcenniejsze reguły.
- Opisuj mechanikę, a nie przymiotniki. Źle: „ciepły, autentyczny ton”. Dobrze: „62% postów zaczyna się od zdania w 1. osobie o porażce, max 8 słów, potem pusta linia”.

## Krok 6: Zbuduj skill `<slug>-voice`

Utwórz:

```
.claude/skills/<slug>-voice/
├── SKILL.md                    ← z templates/voice-skill-template.md, wszystkie {{...}} wypełnione
└── references/
    ├── style-guide.md          ← pełna analiza z kroku 5 (z dowodami)
    └── examples.md             ← 8–12 wzorcowych postów autora
```

**Dobór przykładów w `examples.md`:** głównie top posty, po jednym na każdy typ struktury, w obu językach, jeśli autor pisze w obu. Każdy przykład opatrz jedną linijką: jaki to szablon i dlaczego działa.

**Język PL/EN:** skill ma pisać w obu językach niezależnie od tego, w jakim pisze autor.
- Jeśli autor pisze w jednym języku, przenieś na drugi to, co jest uniwersalne (struktura, rytm, długość, formatowanie, emoji, typy hooków, CTA). Słownictwo i idiomy zbuduj od nowa w duchu autora, bez tłumaczenia kalk. Zapisz to wprost w sekcji „Język” skilla.
- Jeśli pisze w obu, opisz różnice między jego wersją PL i EN (statystyki są w `stats.md` w osobnych sekcjach).

**Opis (`description`) w frontmatterze** musi zawierać frazy wyzwalające po polsku i angielsku: „post w stylu {{Imię}}”, „napisz post jak {{Imię}}”, „{{slug}} style”, „LinkedIn post in {{Imię}}'s style”.

## Krok 7: Test i raport

1. Użyj nowego skilla i napisz 2 posty testowe: jeden PL, jeden EN, na neutralny temat z obszaru autora.
2. Sprawdź oba szkice checklistą z nowego `SKILL.md`. Jeśli coś nie przechodzi, popraw **skill** (reguły, przykłady), a nie tylko szkic, i napisz ponownie.
3. Raport dla użytkowniczki (krótko):
   - ile postów przeanalizowano i z jakiego okresu,
   - 5 najważniejszych cech stylu (z liczbami),
   - jak wywołać nowy skill (np. „napisz post w stylu {{Imię}} o …”),
   - 2 posty testowe,
   - ograniczenia (mało postów, autor pisze tylko w jednym języku, brak grafik itp.).

## Zasady

- Skill naśladuje **mechanikę** stylu. Nie kopiuje historii, faktów z życia, danych, firm ani autorskich sloganów autora. Treść pochodzi zawsze od użytkowniczki.
- Nie twórz treści, które podszywają się pod autora (np. „jako [autor] uważam…”).
- `data/` to surowe dane osoby trzeciej. Nie commituj ich. W skillu zostają tylko przykłady w `examples.md`.
