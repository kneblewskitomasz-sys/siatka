"""siatka — deterministyczny filtr bezpieczenstwa tresci dla tekstu po polsku.

Jedno publiczne API: `sprawdz(tekst)`.

To NIE jest narzedzie medyczne ani terapeutyczne. Filtr wykrywa w surowym
tekscie sygnaly kryzysu, przemocy, naglych stanow medycznych i tresci
niebezpieczne dla dzieci, a w odpowiedzi podaje gotowy komunikat z numerem
pomocy. Nie diagnozuje, nie leczy i nie zastepuje kontaktu z czlowiekiem.
"""

from .dzieci import SiatkaDziecieca
from .kryzys import SiatkaBezpieczenstwa
from .wsparcie import komunikat_wsparcia, komunikat_wsparcia_dzieci, wsparcie

__all__ = [
    "sprawdz",
    "WynikSprawdzenia",
    "SiatkaBezpieczenstwa",
    "SiatkaDziecieca",
    "wsparcie",
    "komunikat_wsparcia",
    "komunikat_wsparcia_dzieci",
]

__version__ = "0.1.0"


class WynikSprawdzenia:
    """Wynik pojedynczego sprawdzenia tekstu przez `sprawdz()`.

    Pola:
      .bezpieczny — bool; False, gdy tekst wyzwolil ktorykolwiek filtr
      .kategoria  — str albo None; np. "kryzys", "przemoc", "medyczny", "dzieci"
      .odpowiedz  — str albo None; tresc, ktora ma pasc zamiast odpowiedzi modelu
    """

    __slots__ = ("bezpieczny", "kategoria", "odpowiedz")

    def __init__(self, bezpieczny: bool, kategoria, odpowiedz):
        self.bezpieczny = bezpieczny
        self.kategoria = kategoria
        self.odpowiedz = odpowiedz

    def __repr__(self) -> str:  # pragma: no cover — pomocnicze
        return (
            f"WynikSprawdzenia(bezpieczny={self.bezpieczny!r}, "
            f"kategoria={self.kategoria!r}, odpowiedz={self.odpowiedz!r})"
        )


_siatka = SiatkaBezpieczenstwa()
_siatka_dzieci = SiatkaDziecieca()


def sprawdz(tekst: str) -> WynikSprawdzenia:
    """Sprawdza tekst wszystkimi warstwami pakietu.

    Kolejnosc jest celowa: kryzys, przemoc i nagly stan medyczny maja
    pierwszenstwo przed tresciami dla dzieci — gdy ktos pisze naraz o bolu
    i o smierci, liczy sie rozmowa z czlowiekiem, nie zabawa. Dopiero gdy
    zadna z tych warstw nie zadziala, sprawdzane sa tresci niebezpieczne
    dla dzieci (seks, przemoc, uzywki, grooming, wulgaryzmy).
    """
    typ = _siatka.sprawdz(tekst)
    if typ:
        return WynikSprawdzenia(
            bezpieczny=False,
            kategoria=typ,
            odpowiedz=_siatka.komunikat(typ),
        )
    if _siatka_dzieci.niebezpieczne(tekst):
        return WynikSprawdzenia(
            bezpieczny=False,
            kategoria="dzieci",
            odpowiedz=_siatka_dzieci.przekierowanie(),
        )
    return WynikSprawdzenia(bezpieczny=True, kategoria=None, odpowiedz=None)
