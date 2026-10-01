# Test results

Run date: 2026-09-30
Environment: Linux, Python 3.12.3, pytest 9.1.1 (the package itself needs
no pytest; each test file also runs standalone with `python`).

## Change under test: input normalisation (PR #2)

`siatka/normalizacja.py` (new, standard library only) runs before every layer —
crisis, violence, medical, support and child:

1. lower-case;
2. `-`, `_` and `.` become a space;
3. every run of whitespace collapses to a single space (and the ends are trimmed);
4. the text is checked in **two** forms, with and without Polish diacritics, and
   every pattern is compiled in both forms too — in all layers, including the
   child filter (which previously did not fold diacritics at all).

One exception: the child pattern `\bgoł[aąeyo]\b` keeps no ASCII form, because
it folds to `gola` ("strzeliłem gola" = "I scored a goal"). This was caught by
the new false-alarm test, not predicted.

Layer scope, categories, response messages and `LICENSE` are unchanged. No new
dependencies.

## Summary

| | Tests | Result |
|---|---|---|
| PR #1 baseline (code before normalisation, old tests) | 16 | 16 passed |
| New tests run against the **old** code | 17 | 15 passed, **2 failed** (`test_biale_znaki_i_interpunkcja`, `test_tryb_dzieci_bez_polskich_znakow`) |
| New tests against the **new** code | 17 | **17 passed** |

New test: `test_zdania_dziecka_bez_alarmu` — 20 ordinary children's sentences
(school, play, food; some without diacritics or with hyphens) must not trigger
any layer, including the non-interrupting support layer. It also passes on the
old code; its job is to guard against false alarms that diacritic folding can
introduce (it caught the `gola` case above).

Speed: about 1.2 ms per `sprawdz()` call on a short sentence (patterns are
now compiled in two forms).

## Known gaps closed by this change (moved to "must catch")

| Input | Before | After |
|---|---|---|
| `nie  chcę   żyć` (repeated spaces) | `dzieci` — child "let's play" reply instead of helpline | `kryzys` |
| `nie-chcę-żyć`, `nie_chce_zyc`, `nie.chce.zyc`, `NIE - CHCĘ - ŻYĆ`, tabs | `dzieci` / not caught | `kryzys` |
| `mąż - mnie - bije` | not caught | `przemoc` |
| `nie mow rodzicom`, `podaj mi swoj adres`, `spotkajmy sie` (grooming, no diacritics) | not blocked | blocked (`dzieci`) |
| `chce wodeczki`, `zapalmy skreta` | not blocked | blocked |
| `nie chce zyc` in the child filter itself | not blocked | blocked (full API already returned `kryzys`) |

## Gaps that REMAIN

Pinned in `tests/test_przypadki_brzegowe.py` as known gaps; a fix makes the
test fail and forces an explicit update.

**Typo inside a word stem** — normalisation does not correct spelling:

| Input | Today | Expected |
|---|---|---|
| `samobujstwo`, `nie myśle o samobujstwie` | not caught | `kryzys` |
| `nie chcem żyć`, `nie hcę żyć`, `nie chcę już żyyyć` | not caught | `kryzys` |
| `chcę się zabć`, `chce sie zabiś` | not caught | `kryzys` |
| `mąż mnie bję` | not caught | `przemoc` |
| `sex`, `s3ks`, `kurva` (child filter) | not blocked | blocked |

**Other remaining gaps:**

| Input | Today | Why it stays |
|---|---|---|
| `nie chcę, żyć` | not caught | commas are deliberately not normalised: `nie, chcę żyć` means the opposite |
| `pokaz gola pania` | not blocked | `goł[aąeyo]` kept diacritics-only to avoid "strzeliłem gola" false alarm |
| `Ubieramy choinkę i wieszamy bombki` | **false alarm** (`dzieci`) | pre-existing `\bbomb\w*` pattern, out of scope (no pattern edits in this PR) |
| `nie grozi mi nic`, `nie mam zawału` | alarm | negation before the phrase is ignored (accepted over-sensitivity) |

Negated crisis statements (`nie myślę o samobójstwie`) still trigger the crisis
response by design.

## Full run (new code)

```
$ python -m pytest -v
tests/test_api.py::test_api PASSED
tests/test_przypadki_brzegowe.py::test_brak_polskich_znakow PASSED
tests/test_przypadki_brzegowe.py::test_biale_znaki_i_interpunkcja PASSED
tests/test_przypadki_brzegowe.py::test_tryb_dzieci_bez_polskich_znakow PASSED
tests/test_przypadki_brzegowe.py::test_zdania_dziecka_bez_alarmu PASSED
tests/test_przypadki_brzegowe.py::test_literowki PASSED
tests/test_przypadki_brzegowe.py::test_przeczenie_kryzys PASSED
tests/test_przypadki_brzegowe.py::test_przeczenie_przemoc_i_medyczne PASSED
tests/test_siatka_bezpieczenstwa.py::test_bierna_ideacja PASSED
tests/test_siatka_bezpieczenstwa.py::test_warstwa_wspierajaca PASSED
tests/test_siatka_bezpieczenstwa.py::test_kryzys PASSED
tests/test_siatka_bezpieczenstwa.py::test_przemoc PASSED
tests/test_siatka_bezpieczenstwa.py::test_bezpieczne PASSED
tests/test_siatka_bezpieczenstwa.py::test_komunikaty PASSED
tests/test_siatka_bezpieczenstwa.py::test_nagle_stany_medyczne PASSED
tests/test_siatka_bezpieczenstwa.py::test_forma_bezosobowa PASSED
tests/test_tryb_dzieci.py::test_tryb_dzieci PASSED
17 passed in 0.14s
```

Standalone runs:

```
$ python tests/test_api.py
✅ API sprawdz(): kryzys, przemoc, medyczny, dzieci, bezpieczny, pusty — OK.

$ python tests/test_przypadki_brzegowe.py
✅ Przypadki brzegowe: 7 grup (ogonki, białe znaki, tryb dzieci, zdania dziecka, literówki, przeczenia) — OK, znane luki bez zmian.

$ python tests/test_siatka_bezpieczenstwa.py
✅ Wszystkie testy przeszły (27 kryzys, 9 przemoc, 11 bezpieczne).
✅ Nagle stany medyczne: 16 alarmowych, 12 przepuszczonych.
✅ Forma bezosobowa: 10 wykrytych, 4 poprawnie przepuszczonych.
✅ Bierna ideacja: 10 wykrytych, 5 poprawnie przepuszczonych, 4 swiadomie poza granica.
✅ Warstwa wspierająca: 6 wykrytych, 8 poprawnie przepuszczonych, kryzys wygrywa 5/5.

$ python tests/test_tryb_dzieci.py
✅ Tryb dzieci: 22 zablokowanych, 11 przepuszczonych.
```
