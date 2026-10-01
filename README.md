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
  już żyć" we wszystkich warstwach, także dziecięcej (tekst i wzorce
  sprawdzane w dwóch postaciach: z ogonkami i bez).
- **Białe znaki i separatory** — „nie  chcę   żyć", „nie-chcę-żyć",
  „nie_chce_zyc" łapane jak „nie chcę żyć" (`siatka/normalizacja.py`).
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
python tests/test_przypadki_brzegowe.py
```

Wymaga wyłącznie Pythona >= 3.12 ze standardowej biblioteki. Działa offline.
Ostatni wynik testów: `TEST_RESULTS.md`.

---

## EN — Installation

Requirements: **Python >= 3.12**. No third-party dependencies, no network
access, no AI model — only `re` and `typing` from the standard library.

The package is not published on PyPI yet. Install it from source:

```bash
git clone https://github.com/kneblewskitomasz-sys/siatka.git
cd siatka
python3.12 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

Or directly from GitHub, without cloning:

```bash
pip install "git+https://github.com/kneblewskitomasz-sys/siatka.git"
```

## EN — Usage

The whole public API is one function, `sprawdz(tekst)` ("check(text)"). Call it
on every user message **before** sending it to your LLM (and, in child mode,
on the model's answer as well):

```python
from siatka import sprawdz

result = sprawdz("nie chcę już żyć")   # "I don't want to live anymore"
result.bezpieczny   # False
result.kategoria    # "kryzys" (crisis)
result.odpowiedz    # ready-made message with a helpline number (116 123 / 112)

sprawdz("jaka jest dziś pogoda?")      # "what's the weather today?"
# -> bezpieczny=True, kategoria=None, odpowiedz=None
```

A typical integration in a chat loop:

```python
from siatka import sprawdz

def answer(user_message: str) -> str:
    result = sprawdz(user_message)
    if not result.bezpieczny:
        # Do NOT call the model. Return the fixed safety message instead.
        return result.odpowiedz
    return call_your_llm(user_message)
```

Text without Polish diacritics works the same way for the crisis, violence and
medical layers — `sprawdz("nie chce juz zyc")` also returns `"kryzys"`.

## EN — What it does

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

## EN — Limitations

- **Polish only.** Patterns, word lists and response messages are written for
  Polish. Text in any other language (including English) passes through as
  "safe" — `sprawdz("I want to die")` returns `bezpieczny=True`. Do not use
  siatka as the only safety layer for a multilingual product.
- **Pattern-based, not understanding-based.** Detection is a fixed list of
  regular expressions and keywords. Consequences:
  - it catches what the patterns describe and nothing else; new slang,
    indirect phrasing or context spread over several messages can be missed;
  - typos *inside* a matched word stem are not caught (`samobujstwo`,
    `nie chcem żyć`); there is no fuzzy matching;
  - it does not parse negation — `nie myślę o samobójstwie` ("I'm not thinking
    about suicide") still triggers the crisis response (intentional:
    over-sensitivity is preferred to a missed crisis);
  - commas are not normalised on purpose (`nie, chcę żyć` means the
    opposite of `nie chcę żyć`), so `nie chcę, żyć` is not caught.

  Input normalisation (`siatka/normalizacja.py`) collapses whitespace, turns
  `-`, `_` and `.` into spaces, and checks every layer both with and without
  Polish diacritics.

  These gaps are pinned in `tests/test_przypadki_brzegowe.py` and listed in
  `TEST_RESULTS.md`, so any change to them is visible.
- **It does not replace a human.** siatka only decides *whether* to stop the
  conversation and *which* fixed message to show. It cannot assess risk,
  follow up, call for help or stay with the person. Every deployment that
  can reach people in crisis needs a human escalation path (moderators,
  trained staff, or at minimum clear information about real helplines), and
  must not advertise the filter as protection.
- **Single message, no memory.** Each call looks at one piece of text in
  isolation; it has no conversation history.
- **Local helplines.** The phone numbers in the messages are valid in Poland
  only.

## EN — Running the tests

```bash
python tests/test_siatka_bezpieczenstwa.py
python tests/test_tryb_dzieci.py
python tests/test_api.py
python tests/test_przypadki_brzegowe.py   # typos, missing diacritics, negation
# or, if pytest is installed:
python -m pytest
```

The tests run on plain `assert` and need nothing beyond Python >= 3.12. The
latest recorded run is in `TEST_RESULTS.md`.

## Project plan / milestones

Planned work for a grant application to **NLnet** (call closing
**3 November 2026**). The goal is to turn siatka from a single-product filter
into a documented, measurable and reusable safety layer for Polish-language
LLM applications, released under Apache-2.0. Durations are estimates of
effort; budget per milestone is to be set in the application.

| # | Milestone | Main deliverables | Est. effort |
|---|---|---|---|
| M1 | **Evaluation corpus & metrics** | Public, anonymised/synthetic Polish test corpus (crisis, violence, medical, child-unsafe, and hard negatives), with recall / false-alarm numbers per category published for each release; CI running all tests on every change. | 1.5 months |
| M2 | **Robustness fixes** | Whitespace/hyphen normalisation in all layers; diacritic folding in the child filter; controlled typo tolerance for high-risk stems (e.g. `samobujstwo`); regression tests for every fixed gap listed in `TEST_RESULTS.md`. | 1.5 months |
| M3 | **Negation & context handling** | Documented rules for negation and reported speech across all layers, keeping the "never miss a crisis" policy; optional multi-message window so signals split across messages (e.g. by speech-to-text) are not lost. | 2 months |
| M4 | **Configurable responses & localisation of helplines** | Response messages and helpline numbers moved to data files, so deployers can adapt them (other countries, institutions) without editing code; message review with people experienced in crisis support. | 1 month |
| M5 | **Packaging & integration** | PyPI release with semantic versioning, typed API reference, integration examples (plain chat loop, voice/STT pipeline, child mode on input and output), and a guide on adding a human escalation path. | 1 month |
| M6 | **Independent review & 1.0 release** | External security/safety review of patterns and bypasses, published findings and fixes, 1.0 release and a short report on measured results against M1 baselines. | 1 month |

Out of scope for this plan: adding an AI model, network calls, or collecting
real user conversations — the project stays deterministic, offline and
dependency-free.

---

## Licencja / License

Apache-2.0 — patrz `LICENSE`.
