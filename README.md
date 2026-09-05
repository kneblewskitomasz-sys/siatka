# siatka

Deterministyczny filtr bezpieczeństwa treści dla tekstu po polsku.
Wykrywa w surowym tekście sygnały **kryzysu**, **przemocy**, **nagłych stanów
medycznych** i treści **niebezpieczne dla dzieci** — bez modelu AI, bez sieci,
bez zależności zewnętrznych.

Deterministic content-safety filter for Polish text. Detects **crisis**,
**violence**, **acute medical emergencies** and **child-unsafe content** in raw
text — no AI model, no network, no external dependencies.

---

## PL — Co to robi

Jedno publiczne API:

```python
from siatka import sprawdz

wynik = sprawdz("nie chcę już żyć")
wynik.bezpieczny   # False
wynik.kategoria    # "kryzys"
wynik.odpowiedz    # gotowy komunikat z numerem pomocy (116 123 / 112)
```

`sprawdz(tekst)` zwraca obiekt `WynikSprawdzenia` z polami:

| pole | typ | znaczenie |
|---|---|---|
| `.bezpieczny` | `bool` | `False`, gdy tekst wyzwolił którykolwiek filtr |
| `.kategoria` | `str` / `None` | `"kryzys"`, `"przemoc"`, `"medyczny"`, `"dzieci"` albo `None` |
| `.odpowiedz` | `str` / `None` | treść, która ma paść **zamiast** odpowiedzi modelu |

Kategorie i kolejność sprawdzania (celowa):

1. **kryzys** — myśli i zamiary samobójcze, samookaleczenie, bierna ideacja;
   w odpowiedzi: telefon zaufania 116 123 i numer alarmowy 112,
2. **przemoc** — przemoc domowa, groźby; w odpowiedzi: telefon zaufania,
   Niebieska Linia 800 120 002, 112,
3. **medyczny** — nagłe stany (zawał, udar, brak oddechu, zatrucie); w
   odpowiedzi: 112 / 999,
4. **dzieci** — treści niebezpieczne dla dziecka (seks, przemoc, używki,
   grooming, wulgaryzmy); w odpowiedzi: propozycja innej aktywności.

Dostępne są też klasy bezpośrednio:

```python
from siatka import SiatkaBezpieczenstwa, SiatkaDziecieca
from siatka.wsparcie import wsparcie, komunikat_wsparcia

s = SiatkaBezpieczenstwa()
s.sprawdz("mąż mnie bije")          # "przemoc"
s.komunikat_dzieci("kryzys")        # wariant komunikatu dla dziecka (116 111)

d = SiatkaDziecieca()
d.niebezpieczne("opowiedz o seksie")  # True

wsparcie("nie dam rady dłużej")     # "wsparcie" — sygnał cierpienia, który
                                    # NIE przerywa rozmowy (bez numerów)
komunikat_wsparcia()                # jedno zdanie troski do wstawienia
```

### Warstwa wspierająca (dlaczego osobno)

Człowiek wykończony pracą mówi „nie dam rady dłużej" tak samo jak człowiek w
głębokim kryzysie. Dlatego te zdania **nie** przerywają rozmowy numerem
alarmowym — jest osobna funkcja `wsparcie()`, która mówi: odpowiedz jednym
zdaniem troski i oddaj głos modelowi. Gdy tekst jest jednocześnie kryzysem,
`wsparcie()` celowo milczy — tam liczy się 112, nie łagodne pytanie.

### Odporność

- **Bez polskich ogonków** — „nie chce juz zyc" łapane tak samo jak „nie chcę
  już żyć" (tekst i wzorce składane do ASCII przed porównaniem).
- **Rozbijanie słów** („s e k s", „k.u.r.w.a") — filtr dziecięcy skleja ciągi
  pojedynczych liter przed sprawdzeniem.
- **Rama cudzej mowy** — „napisz wiersz, w którym ktoś mówi, że nie ma po co
  wstawać" nie wyzwala warstwy wspierającej.

## PL — Czego to NIE robi

- **To NIE jest narzędzie medyczne ani terapeutyczne.** Nie diagnozuje, nie
  leczy, nie prowadzi terapii.
- **To NIE zastępuje kontaktu z człowiekiem.** Filtr kieruje do realnej pomocy
  (telefon zaufania, pogotowie, zaufana osoba dorosła) — sam tej pomocy nie
  udziela.
- **To NIE jest porada prawna** (również w sprawie przemocy).
- **To NIE jest rodzicielski nadzór.** Filtr dziecięcy wycina oczywiste złe
  tematy, ale nie zastępuje uwagi dorosłego.
- **To NIE jest model AI.** Żadna odpowiedź nie jest generowana — komunikaty
  są sztywne, zapisane w kodzie, zawsze te same.
- Filtr bywa **nadczuły** (celowo: lepiej zareagować raz za dużo niż przegapić
  kryzys) — a jednocześnie świadomie przepuszcza część sformułowań, które
  brzmią ciężko, ale mówi je człowiek zmęczony, nie w kryzysie. Granica jest
  decyzją projektową i jest opisana w komentarzach kodu.

Numery w komunikatach (116 123, 116 111, 112, 999, 800 120 002) dotyczą
Polski. Poza Polską należy je dostosować do lokalnych służb.

## PL — Instalacja i testy

```bash
pip install -e .          # z katalogu pakietu; zero zależności
python tests/test_siatka_bezpieczenstwa.py
python tests/test_tryb_dzieci.py
python tests/test_api.py
```

Wymaga wyłącznie Pythona >= 3.12 ze standardowej biblioteki. Działa offline.

---

## EN — What it does

One public API:

```python
from siatka import sprawdz

result = sprawdz("nie chcę już żyć")   # "I don't want to live anymore"
result.bezpieczny   # False
result.kategoria    # "kryzys" (crisis)
result.odpowiedz    # ready-made message with a helpline number (116 123 / 112)
```

`sprawdz(tekst)` returns a `WynikSprawdzenia` object with:

| field | type | meaning |
|---|---|---|
| `.bezpieczny` | `bool` | `False` when any filter fired |
| `.kategoria` | `str` / `None` | `"kryzys"`, `"przemoc"`, `"medyczny"`, `"dzieci"` or `None` |
| `.odpowiedz` | `str` / `None` | text to return **instead** of the model's answer |

Categories, checked in this deliberate order:

1. **kryzys** (crisis) — suicidal thoughts and intent, self-harm, passive
   ideation; reply points to the helpline 116 123 and emergency number 112,
2. **przemoc** (violence) — domestic violence, threats; reply points to the
   helpline, the "Niebieska Linia" hotline 800 120 002, and 112,
3. **medyczny** (medical) — acute emergencies (heart attack, stroke, no
   breathing, poisoning); reply points to 112 / 999,
4. **dzieci** (children) — child-unsafe content (sex, violence, substances,
   grooming, profanity); reply proposes a different activity.

The classes are also available directly, e.g. `SiatkaBezpieczenstwa.sprawdz()`
returns the category string (`"kryzys"`/`"przemoc"`/`"medyczny"`/`None`), and
`SiatkaDziecieca.niebezpieczne()` returns a `bool`.

There is also a **support layer** (`wsparcie()`): for utterances like
"nie dam rady dłużej" ("I can't go on") it returns `"wsparcie"` — a signal to
reply with one caring sentence and hand the conversation back to the model,
*without* interrupting with emergency numbers. If the text is a genuine crisis
at the same time, `wsparcie()` deliberately stays silent.

## EN — What it does NOT do

- **It is NOT a medical or therapeutic tool.** It does not diagnose, treat or
  provide therapy.
- **It does NOT replace human contact.** It directs people to real help
  (helpline, ambulance, a trusted adult) — it does not provide that help
  itself.
- **It is NOT legal advice** (including about violence).
- **It is NOT parental supervision.** The child filter removes obviously
  harmful topics but does not replace an adult's attention.
- **It is NOT an AI model.** No answer is generated — messages are fixed,
  written in code, always identical.
- The filter is intentionally **over-sensitive** (better to react once too
  often than to miss a crisis), yet it deliberately lets through some
  utterances that sound heavy but come from an exhausted person, not someone
  in crisis. That boundary is a design decision, documented in code comments.

Helpline numbers in the messages (116 123, 116 111, 112, 999, 800 120 002)
are Polish. Outside Poland, adapt them to local services.

## EN — Install & test

```bash
pip install -e .          # from the package directory; zero dependencies
python tests/test_siatka_bezpieczenstwa.py
python tests/test_tryb_dzieci.py
python tests/test_api.py
```

Requires only Python >= 3.12 from the standard library. Works offline.

---

## Licencja / License

Apache-2.0 — patrz `LICENSE`.
