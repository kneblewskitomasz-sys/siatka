"""Warstwa wspierajaca — sygnal cierpienia, ktory NIE przerywa rozmowy.

Roznica miedzy `sprawdz()` (modul glowny) a ta warstwa:
`sprawdz()` wykrywa sytuacje, w ktorych rozmowa ma zostac PRZERWANA
(kryzys, przemoc, nagly stan medyczny) i w jej miejsce ma pasc numer
pomocy. Ta warstwa wykrywa sygnaly cierpienia, na ktore asystent ma sie
odezwac jednym zdaniem troski, ale NIE przerywac rozmowy — model odpowiada
dalej.

Tej warstwy nie wolno uzywac zamiast `sprawdz()`: gdy tekst jest
jednoczesnie kryzysem, ta funkcja swiadomie milczy, bo tam liczy sie
numer alarmowy, nie lagodne pytanie.
"""

from typing import Optional

from .kryzys import SiatkaBezpieczenstwa

_siatka = SiatkaBezpieczenstwa()


def wsparcie(tekst: str) -> Optional[str]:
    """Zwraca 'wsparcie', gdy tekst jest sygnalem cierpienia, albo None.

    Sygnal znaczy: odpowiedz jednym zdaniem troski (patrz
    `komunikat_wsparcia`) i oddaj glos modelowi. Kryzys, przemoc i nagly
    stan medyczny maja pierwszenstwo — dla nich ta funkcja zwraca None,
    a odezwac powinien sie `sprawdz()` z numerem pomocy.
    """
    return _siatka.wsparcie(tekst)


def komunikat_wsparcia() -> str:
    """Jedno zdanie troski dla doroslego rozmowcy (bez numerow alarmowych)."""
    return _siatka.komunikat_wsparcia()


def komunikat_wsparcia_dzieci() -> str:
    """Jedno zdanie troski dla dziecka (odeslanie do rodzica, bez infolinii)."""
    return _siatka.komunikat_wsparcia_dzieci()
