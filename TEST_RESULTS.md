# Test results

Run date: 2026-09-24
Environment: Linux, Python 3.12.3, pytest 9.1.1 (the package itself needs
no pytest; each test file also runs standalone with `python`).

Note: the default `python3` in the test environment was 3.11, but the package
declares `requires-python = ">=3.12"`, so tests were run in a Python 3.12
virtual environment.

## Before this change (existing tests only)

```
$ python -m pytest -v
tests/test_api.py::test_api PASSED
tests/test_siatka_bezpieczenstwa.py::test_bierna_ideacja PASSED
tests/test_siatka_bezpieczenstwa.py::test_warstwa_wspierajaca PASSED
tests/test_siatka_bezpieczenstwa.py::test_kryzys PASSED
tests/test_siatka_bezpieczenstwa.py::test_przemoc PASSED
tests/test_siatka_bezpieczenstwa.py::test_bezpieczne PASSED
tests/test_siatka_bezpieczenstwa.py::test_komunikaty PASSED
tests/test_siatka_bezpieczenstwa.py::test_nagle_stany_medyczne PASSED
tests/test_siatka_bezpieczenstwa.py::test_forma_bezosobowa PASSED
tests/test_tryb_dzieci.py::test_tryb_dzieci PASSED
10 passed in 0.11s
```

## After this change (with `tests/test_przypadki_brzegowe.py`)

```
$ python -m pytest -v
tests/test_api.py::test_api PASSED
tests/test_przypadki_brzegowe.py::test_brak_polskich_znakow PASSED
tests/test_przypadki_brzegowe.py::test_biale_znaki_i_interpunkcja PASSED
tests/test_przypadki_brzegowe.py::test_tryb_dzieci_bez_polskich_znakow PASSED
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
16 passed in 0.10s
```

Standalone runs (no pytest):

```
$ python tests/test_api.py
✅ API sprawdz(): kryzys, przemoc, medyczny, dzieci, bezpieczny, pusty — OK.

$ python tests/test_siatka_bezpieczenstwa.py
✅ Wszystkie testy przeszły (27 kryzys, 9 przemoc, 11 bezpieczne).
✅ Nagle stany medyczne: 16 alarmowych, 12 przepuszczonych.
✅ Forma bezosobowa: 10 wykrytych, 4 poprawnie przepuszczonych.
✅ Bierna ideacja: 10 wykrytych, 5 poprawnie przepuszczonych, 4 swiadomie poza granica.
✅ Warstwa wspierająca: 6 wykrytych, 8 poprawnie przepuszczonych, kryzys wygrywa 5/5.

$ python tests/test_tryb_dzieci.py
✅ Tryb dzieci: 22 zablokowanych, 11 przepuszczonych.

$ python tests/test_przypadki_brzegowe.py
✅ Przypadki brzegowe: 6 grup (ogonki, białe znaki, tryb dzieci, literówki, przeczenia) — OK, znane luki bez zmian.
```

## Known gaps found by the edge-case tests

The new tests pin these as *known gaps* (they assert today's behaviour, so an
improvement to the filter makes the test fail and forces an explicit update).
No filter code was changed in this PR.

| Input | Today | Expected | Why |
|---|---|---|---|
| `nie  chcę   żyć` (double spaces) | `dzieci` | `kryzys` | crisis patterns use a literal space after `nie`; the child filter then catches it and replies with "let's play" instead of a helpline |
| `nie-chcę-żyć` | `dzieci` | `kryzys` | same cause |
| `nie mow rodzicom`, `podaj mi swoj adres`, `spotkajmy sie` | not blocked | blocked (grooming) | the child filter does not fold Polish diacritics, unlike the crisis filter |
| `pokaz gola pania`, `chce wodeczki`, `zapalmy skreta` | not blocked | blocked | same cause |
| `samobujstwo`, `nie chcem żyć`, `chcę się zabć`, `mąż mnie bję` | not caught | caught | typo inside the matched word stem; patterns have no fuzzy matching |
| `sex`, `s3ks`, `kurva` | not blocked | blocked | English spelling / leetspeak / Czech-style spelling not in the word list |
| `nie grozi mi nic`, `nie mam zawału` | alarm | no alarm | negation before the phrase is ignored (accepted over-sensitivity) |

Negated crisis statements (`nie myślę o samobójstwie`, `nie chcę się zabić`)
still trigger the crisis response. This is a documented design decision
(better one false alarm than a missed crisis) and is asserted as intended
behaviour, not as a gap.
