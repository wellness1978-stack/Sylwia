# Wzorcowe posty: Łukasz Podgórski

Dosłowne posty autora jako wzorzec mechaniki. **Nie kopiuj zdań, historii ani faktów.** Patrz na strukturę, rytm, formatowanie i sposób zwracania się do czytelnika.

## 1. B. Eksperyment z liczbami

**Dlaczego działa:** Nr 2 w rankingu. Wynik liczbowy w pierwszym zdaniu, prosta metoda, ponumerowane wnioski, zastrzeżenie metodyczne, pytanie z obietnicą (dorzucę Twój sprzęt do testu).  
`id 7520586621373640704 · 2026-10-26 · image · 👍 80 💬 11 🔁 3`

```text
Uruchomiłem ten sam model AI na siedmiu różnych urządzeniach, od małej płytki Raspberry Pi 5 po stację HP ZGX Nano AI. Trafność była wszędzie taka sama, około 74%. Sprzęt zmieniał tylko to, jak długo czekamy na odpowiedź: od 10 milisekund do 3 sekund.

Testowałem basala, polski model decyzyjny. Ten model nie pisze tekstów, tylko podejmuje decyzje. Dostaje tekst i zamknięte pytanie, a zwraca wybór razem z pewnością. Sprawdza się przy routingu zgłoszeń, filtrowaniu wpisów czy rozpoznawaniu poleceń w inteligentnym domu.

Na każdym urządzeniu model odpowiadał na dokładnie te same 1000 pytań z sześciu polskich zbiorów testowych. Dzięki temu wyniki da się porównać jeden do jednego.

Pierwszy wniosek: jakość odpowiedzi zależy od modelu, a nie od sprzętu. 

Skwantyzowana wersja uruchomiona na zwykłym procesorze trafia tak samo często jak pełna wersja na karcie graficznej. Różnice mieszczą się w granicach błędu pomiaru.

Trzeci wniosek był dla mnie najciekawszy: niski pobór mocy nie oznacza niskiego zużycia energii. Mini PC z Intelem N100 pobiera zaledwie 10 W, ale liczy tak długo, że na jedną decyzję zużywa najwięcej energii ze wszystkich urządzeń: 62,5 J. Najoszczędniejszy okazał się HP ZGX Nano AI. Potrzebuje 2,2 J na decyzję, czyli prawie trzydzieści razy mniej.

Osobne słowo o Raspberry Pi 5. To sprzęt, który mam od dawna, więc z ciekawości dorzuciłem go do testu. Bez karty graficznej basal liczy na nim jedną decyzję w 1,9 sekundy, zajmuje 2,4 GB pamięci i trafia w 74% przypadków, dokładnie tak jak na dużej stacji z GPU. To około 1700 decyzji na godzinę. Pi okazało się nawet szybsze od Intela N100, który na tym samym modelu potrzebował 3 sekund.

Z tego testu wynika jedna praktyczna rzecz. Wybierając sprzęt pod mały model, wybierasz czas odpowiedzi i rachunek za prąd, a nie jakość decyzji.

Ważne zastrzeżenie: to pokaz możliwości, a nie ranking zakupowy. Sprawdzałem, co da się uruchomić i z jakim efektem na sprzęcie, który akurat mam pod ręką. Dobór urządzenia do konkretnego wdrożenia zależy od ruchu, budżetu i tego, co już stoi w szafie.

Całość opisałem na blogu: metodykę, pełne tabele dla 7 modeli na 7 urządzeniach, wykresy czasu i energii oraz listę ograniczeń testu. Link znajdziesz w pierwszym komentarzu.

Na czym Ty uruchamiasz małe modele? Jeśli masz sprzęt spoza tej listy, daj znać w komentarzu, a dorzucę go do następnej serii testów.

#AI #EdgeAI #RaspberryPi #LLM
```

## 2. A. Wypuściłem (launch)

**Dlaczego działa:** TL;DR po hooku, „Pomysł był prosty”, lista cech z emoji-punktorami, jedna wyróżniona wartość („A najważniejsze: 🔒 zero chmury”), konkretny adresat, prośba o feedback.  
`id 7478476046191996928 · 2026-07-02 · image · 👍 47 💬 8 🔁 1`

```text
🚀 Mała rzecz, a cieszy: moja wtyczka AitoMail for Thunderbird została właśnie opublikowana w oficjalnym sklepie z dodatkami Thunderbirda!

TL;DR: podsumowuje e-maile i generuje szkice odpowiedzi za pomocą lokalnego modelu AI (przez Ollama api). Wszystko działa na Twoim komputerze, więc żadne dane nie trafiają do chmury.

Pomysł był prosty: chciałem mieć AI w skrzynce mailowej, ale bez wysyłania korespondencji do chmury. Tak powstał AitoMail - asystent AI, który działa w 100% lokalnie, na Twoim komputerze, w oparciu o Ollama.

Co potrafi?
📄 Podsumowania e-maili - długi wątek zamienia w 3–5 zdań z kluczowymi informacjami, zadaniami i terminami

✍️ Szkice odpowiedzi - jednym kliknięciem generuje uprzejmą, profesjonalną odpowiedź i otwiera ją od razu w oknie tworzenia wiadomości

📚 Baza wiedzy - dodaj własny kontekst (informacje o firmie, procedury, FAQ z plików .txt, .md lub .csv), a odpowiedzi będą trafne i spójne z Twoją marką

⚙️ Konfigurowalne prompty i dowolny model z Twojej instalacji Ollama (Bielik, Gemma, GPT-OSS, Llama, Mistral, Phi...)

🌍 Interfejs w 8 językach

A najważniejsze: 🔒 zero chmury. Bez kluczy API, bez subskrypcji, bez telemetrii. Twoje e-maile nigdy nie opuszczają Twojego komputera.

Komu się przyda? Każdemu, kto pracuje na Thunderbirdzie i dostaje dużo maili - a szczególnie osobom i firmom, które ze względu na poufność danych (prawnicy, księgowi, HR, medycyna, administracja) nie mogą lub nie chcą korzystać z chmurowych narzędzi AI.
Wystarczy Thunderbird 78+, zainstalowana Ollama i jeden pobrany model.

Będę wdzięczny za każdą opinię, komentarz i udostępnienie! 🙏

#AI #Thunderbird #Ollama #Privacy #LocalLLM #Productivity
```

## 3. A. Wypuściłem (wersja krótka)

**Dlaczego działa:** Launch w 5 akapitach: co to, jak działa, efekt w liczbach, szczere „to dopiero początek”, zaproszenie do issues.  
`id 7521231523698851840 · 2026-10-28 · image · 👍 60 💬 4 🔁 2`

```text
Wypuściłem wczesną wersję basal-lite 🚀

Basal od Remigiusz Kinas to modele (oraz dodatkowa warstwa zarządzająca), które zamiast generować tekst podejmują decyzje: dostają np. wiadomość klienta i pytania z opcjami, a zwracają skalibrowane prawdopodobieństwa.

basal-lite pozwala serwować je ze zwykłego 'vllm serve' - cała logika basala (prompty, kalibracja, typy pytań, obrazy, audio) siedzi w małym kliencie w Pythonie. 

Efekt: te same decyzje co oficjalny basal-serve, do 2,2x szybciej na mediach i jeden serwer vLLM współdzielony z innymi aplikacjami.

To dopiero początek – kod na pewno będzie jeszcze poprawiany. Feedback i issues bardzo mile widziane!
```

## 4. C. Przełom osobisty

**Dlaczego działa:** Nr 3. Zwrot „Ale dziś chcę podzielić się czymś innym”, wrażliwość w krótkich zdaniach, autoironiczne nawiasy, „I wiecie co? Zrobiłem to.”  
`id 7386785600932163586 · 2025-10-22 · image · 👍 67 💬 16 🔁 0`

```text
21 października 2025 roku stanąłem na scenie jako prelegent, podczas  III edycja Spotkania Ekspertów BHP Santander Bank Polska.

Mówiłem o sztucznej inteligencji w bezpieczeństwie pracy - o jej możliwościach, pułapkach i niebezpieczeństwach. O tym, jak ważne jest krytyczne myślenie na każdym etapie korzystania z narzędzi AI. O tym, że rozwój technologii otwiera przed nami niesamowite możliwości, ale wymaga też świadomości i odpowiedzialności.

Ale dziś chcę podzielić się czymś innym.
Największym wyzwaniem nie był zakres merytoryczny mojej prelekcji. Największym wyzwaniem było stanięcie przed ludźmi. Pokonanie strachu. Zmierzenie się z lękiem przed publicznym wystąpieniem, który towarzyszył mi od lat. (introwertyk z IT 😉)

I wiecie co? Zrobiłem to.
Nie było idealnie. Serce biło jak szalone, ręce drżały. (garmin alertował kilka razy o zbyt wysokim HR) Ale stanąłem tam i powiedziałem to, co miałem do powiedzenia.

Dziękuję za zaufanie i możliwość sprawdzenia się w tej nowej dla mnie roli.

Małgorzata Furtak Matylda Kawczyńska Mateusz Starke Daniel Trybus 

#ai #BHP #Santander
```

## 5. D. Szukam ludzi

**Dlaczego działa:** 26 komentarzy. Jasno kogo i po co, „nie szukam mentora”, 3 kryteria, CTA do wiadomości prywatnej z konkretną instrukcją.  
`id 7496535025732124672 · 2026-08-21 · image · 👍 32 💬 26 🔁 2`

```text
Szukam pasjonatów AI do nieformalnego grona wymiany doświadczeń

---
UPDATE: Można się zgłaszać tutaj: https://lnkd.in/dbHvg_H2 :)
---


Cześć! Szukam osób, dla których sztuczna inteligencja to nie tylko przelotna moda, ale prawdziwa pasja i obszar, w którym na co dzień aktywnie działają oraz promują nowe technologie.

Zależy mi na stworzeniu zgranego, nieformalnego zespołu praktyków. Nie szukam mentora czy nauczyciela - zależy mi na gronie równorzędnych partnerów do wymiany doświadczeń, testowania odważnych hipotez i zderzania ze sobą pomysłów.

Kogo dokładnie poszukuję?

- Prawdziwych pasjonatów AI, którzy "siedzą w temacie" i na bieżąco śledzą rynkowe nowości.

- Osób z zapleczem technicznym - mile widziane umiejętności programistyczne lub administratorskie (niestety na rynku wciąż trudno o pasjonatów łączących wizję z twardymi umiejętnościami).

- Inicjatorów, którzy chcą budować przestrzeń wzajemnego wsparcia, dzielić się sukcesami i wspólnie rozwiązywać techniczne zagadki.

Jeśli bliskie Ci jest takie podejście i czujesz, że chcesz dołączyć do grupy ludzi nadających na tych samych falach, daj znać o sobie w wiadomości prywatnej i napisz krótko, czym obecnie się zajmujesz w świecie AI.

#sztucznainteligencja #ai #aipolska #genai
```

## 6. E. Apel do marki: problem → rozwiązanie

**Dlaczego działa:** Nr 1 w rankingu (23 komentarze). Apel z imienia, etykiety „Problem:” / „Rozwiązanie?”, jedno słowo WIELKIMI, empatia wobec adresata, „Pomyślcie o tym ;-)”.  
`id 7389959368479506432 · 2025-10-31 · text · 👍 69 💬 23 🔁 0`

```text
Hej InPost / Rafał Brzoska! Brakuje mi na rynku prostej usługi kurierskiej: możliwości zakupu pakietu wysyłek (np. 10 sztuk) z góry, na jedną fakturę.

Problem: Chcę kupić pakiet teraz (np. by zamknąć budżet, nie spędzać czasu na każdorazowym zamówieniu), ale adresy wysyłki będę znał dopiero za jakiś czas (np. w ciągu 2 miesięcy).

Niestety, strony www i aplikacje wymagają podania adresu W MOMENCIE zakupu, co blokuje ten proces.

Rozwiązanie? Sprzedawajcie po prostu pakiety kodów prepaid (np. 10 kodów na 10 wysyłek), które można wykorzystać w dowolnym terminie.
Wiem, że 10 sztuk to dla Was może niewiele, ale dla mniejszych firm taka elastyczność w budżetowaniu jest naprawdę ważna. 
W moim przypadku muszę teraz szukać innej drogi.
Pomyślcie o tym ;-)

Tutaj sprzedaż kodów rabatowych, które można wpisać przy składaniu zamówienia też jest świetną opcją. Przecież macie takie rozwiązanie przy konkursach - rabatowanie do 0zł.

#inpost #kurier
```

## 7. F. Obserwacja w krótkich akapitach

**Dlaczego działa:** Anegdota → teza → kontrast Kiedyś/Dziś → para równoległych akapitów → jednozdaniowe puenty → otwarte pytanie.  
`id 7500098765534625792 · 2026-08-31 · image · 👍 15 💬 5 🔁 0`

```text
Ktoś napisał do mnie z pomysłem na aplikację mobilną generującą wideo z AI... Na telefonie. Bez obsługi GenAI, bez API, bez bazy danych, bez kolejkowania, bez rate limitów.

Nie było w tym złej woli. Ta osoba po prostu nie wiedziała, że to niewykonalne.

I to jest chyba najciekawsza zmiana ostatnich lat w tworzeniu oprogramowania.

Kiedyś wąskim gardłem było zbudowanie czegokolwiek. Między pomysłem a klikającą się rzeczą stała ściana i firmy, które umiały ją przebić, miały z czego żyć.

Dziś "klikalny" prototyp to kwestia wieczoru. Ludzie robią sobie narzędzia, które wcześniej były poza zasięgiem, i to jest dobre. (Już nie mówię o tym, że centrują "diva" przy pomocy operacji przetwarzającej miliony tokenów :D)

Tylko środek ciężkości się przesunął.

Front jest widoczny. Widać, czy przycisk jest na miejscu, więc AI robi go świetnie, bo efekt da się ocenić okiem.

Backend jest niewidoczny. Nie widać, czy klucze API są bezpieczne, czy przy stu użytkownikach to się nie wywróci, czy dane w ogóle zapisują się sensownie.

Nie widać, więc nie ma sygnału, że czegoś brakuje.

Dlatego tyle świetnych stron z Lovable kończy się w momencie publikacji. Szablon ładny, wszystko klika, jest poczucie "mam to". A potem domena, zmienne środowiskowe, klucze, które nagle nie mogą siedzieć we froncie, i pytanie "dlaczego działało lokalnie".

Rola dewelopera się nie skurczyła. Przesunęła się.

Z "ten, kto to napisze" na "ten, kto powie, czy to w ogóle może działać, i co musi być po stronie serwera".

To są pytania, na które AI nie odpowie, bo AI odpowiada na to, o co pytasz. A problem polega na tym, że nie wiesz jeszcze, o co zapytać.

Widzicie to samo u siebie?
```

## 8. G. News / przegląd zmian

**Dlaczego działa:** 🚨 w hooku, „Dobra wiadomość? / Zła wiadomość?”, sekcje z nagłówkami emoji + WIELKIE LITERY, punkty „→”, konkretne kroki do zrobienia.  
`id 7401705291429609473 · 2025-12-02 · image · 👍 33 💬 6 🔁 0`

```text
🚨 n8n 2.0 nadchodzi - największa aktualizacja od 2 lat!

Za tydzień (8 grudnia - beta, 15 grudnia - stable) pojawi się n8n 2.0 i to nie jest zwykły update. To fundamentalna zmiana platformy.

Dobra wiadomość? 
AUTOSAVE wreszcie będzie dostępny! 🎉
Plus nowy canvas i sidebar.

Zła wiadomość? Jest sporo zmian, które mogą popsuć coś co teraz działa bezproblemowo. Tak więc musisz się przygotować.

Oto co może zepsuć Twoje workflow:

🔴 Do sprawdzenia:
→ Koniec MySQL/MariaDB - musisz zmigrować do PostgreSQL
→ Python Code Node wymaga task runnerów w external mode
→ Subworkflow z Wait Node zwraca teraz INNE dane (output z końca zamiast input do Wait)

🔒 BEZPIECZEŃSTWO (domyślnie włączone):
→ Blokada process.env w Code Node
→ ExecuteCommand i LocalFileTrigger wyłączone
→ Dostęp do plików tylko z katalogu ./data
→ OAuth callback wymaga autoryzacji

❌ USUNIĘTE:
→ n8n --tunnel (używaj ngrok/Cloudflare Tunnel) - polecam cloudflared
→ Nody: Spontit, crowd.dev, Kitemaker
→ In-memory binary data mode

✅ CO BĘDZIE LEPIEJ:
→ SQLite do 10x szybszy (nowy pooling driver)
→ Task runners = izolacja kodu = większe bezpieczeństwo
→ Stabilniejszy filesystem mode dla binary data

📋 CO ZROBIĆ TERAZ:

1. Zaktualizuj do 1.121.0+
2. Wejdź w Settings → Migration Report
3. Przejrzyj listę problemów
4. Masz 3 miesiące na migrację (potem 1.x = tylko security fixes)

Pełna dokumentacja zmian: https://lnkd.in/eCzG46Hf

Czy jesteś przygotowany do migracji, do 2.0?

#n8n #automatyzacja #nocode #lowcode #workflow #AI
```

## 9. Kontrast w hooku + zaproszenie eksperta

**Dlaczego działa:** Dwulinijkowy kontrast, metafora („kartka… na drzwiach od sejfu”), 4 punkty 🔒, pytanie z trzema opcjami.  
`id 7404605522873733122 · 2025-12-10 · image · 👍 19 💬 9 🔁 2`

```text
Wydajesz tysiące na firewalle i VPN-y.
A Twój chatbot wyśpiewa sekrety firmy za darmo.

To realne przypadki ataków na firmowe AI.
Prompt systemowy? To nie firewall. To bardziej jak kartka z napisem "Proszę nie wchodzić" na drzwiach od sejfu.

Dlatego zaprosiłem Tomasz Bartel – eksperta cyberbezpieczeństwa i twórcę Vigil Guard. 

Polskiego narzędzia open-source, które:
🔒 Działa jako proxy między użytkownikiem a LLM-em
🔒 Wycina dane wrażliwe (PII/RODO) w locie
🔒 Blokuje prompt injection zanim dotrze do modelu
🔒 Nie wymaga GPU – działa na zwykłym CPU

Demo na żywo, konkretne ataki, realne zabezpieczenia.
Link do materiału w pierwszym komentarzu 👇
A teraz pytanie do Was:
Czy w Waszej firmie ChatGPT jest zablokowany, dozwolony, czy... nikt o tym nie pomyślał?

#ai #promptinjection #sztucznainteligencja #promptowanie #chatbot
```

## 10. Start side projectu z humorem

**Dlaczego działa:** Hook-cytat, autoironia („odkurzacz z czkawką”), „Spoiler:”, plan w 3 punktach 🔹, zaproszenie do śledzenia postępów.  
`id 7479784735859433472 · 2026-07-06 · image · 👍 9 💬 7 🔁 0`

```text
"A gdyby tak stworzyć własny MAŁY model TTS?" 🎙️

Potrzymaj mi ... DZIKA (skoro już polonizacja?)?

Tak to się zaczyna. Niewinna myśl w niedzielny wieczór. Przecież to "tylko" zamiana tekstu na mowę, prawda? Ile to może być roboty?

Spoiler: dużo. Ale właśnie dlatego warto.

Plan jest prosty:
🔹 mały model, nie kolejny gigant na 100 GPU
🔹 polski język, bo angielskich TTS-ów jest jak mrówków
🔹 działający lokalnie, bez wysyłania głosu w chmurę

Po drodze na pewno będzie moment, w którym model zamiast "dzień dobry" powie coś, co brzmi jak odkurzacz z czkawką. I to też będzie sukces - bo odkurzacz z czkawką to już jakiś głos. 

Będę wrzucał postępy. Jeśli ktoś już przechodził tę drogę - chętnie posłucham.

#TTS #AI #MachineLearning #SideProject #NLP
```

## 11. EN: krótkie ogłoszenie

**Dlaczego działa:** Jedyny dłuższy post EN: rzeczowo, dywiz ze spacjami, fakty bez hype’u.  
`id 7519882831884546048 · 2026-10-24 · image · 👍 21 💬 1 🔁 1`

```text
I've joined MEGA - a four-week program on rethinking how we build, with Theo Browne, Angie Jones, Kent C. Dodds and John Lindquist. Starts October 26. mega.dev
```
