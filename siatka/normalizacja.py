"""Wspolna normalizacja wejscia dla wszystkich warstw filtra.

Kazda warstwa (kryzys, przemoc, medyczny, wsparcie, dzieci) dostaje ten sam
tekst w tej samej postaci, zanim porowna go z wzorcami:

  1. male litery,
  2. myslnik, podkreslnik i kropka -> spacja ("nie-chce-zyc", "nie_chce_zyc"),
  3. kazdy ciag bialych znakow -> jedna spacja ("nie  chce\\t zyc"), bez spacji
     na poczatku i koncu,
  4. DWIE wersje: z polskimi znakami i bez nich. Sprawdzamy obie.

DLACZEGO NORMALIZACJA, A NIE POPRAWKI WZORCOW: wzorce pisane sa dla jednej
spacji ("nie " + _CHCE). Podwojna spacja albo myslniki omijaly warstwe
kryzysowa, a zdanie wpadalo do filtra dzieciecego, ktory odpowiadal
"Pobawmy sie w cos fajnego!" zamiast 116 123. Normalizacja w jednym miejscu
zamyka te klase luk dla wszystkich wzorcow naraz, bez dopisywania wariantow.

Czego tu celowo NIE ma: przecinka (zmienia sens: "nie, chce zyc") ani
poprawiania literowek - te zostaja znanymi lukami.
"""

import re

_DIAKRYTYKI = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
_SEPARATORY = re.compile(r"[-_.]")
_BIALE = re.compile(r"\s+")


def bez_diakrytykow(tekst: str) -> str:
    """Sklada polskie diakrytyki do ASCII (ą->a, ż->z, ...)."""
    return tekst.translate(_DIAKRYTYKI)


def normalizuj(tekst: str) -> str:
    """Male litery, separatory -> spacja, zwiniete biale znaki."""
    t = _SEPARATORY.sub(" ", tekst.lower())
    return _BIALE.sub(" ", t).strip()


def warianty(tekst: str) -> tuple[str, ...]:
    """Znormalizowany tekst w wersji z diakrytykami i bez (bez duplikatow)."""
    t = normalizuj(tekst)
    ascii_ = bez_diakrytykow(t)
    return (t,) if ascii_ == t else (t, ascii_)
