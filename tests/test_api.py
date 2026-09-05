"""Testy publicznego API pakietu: siatka.sprawdz(tekst).

Uruchom:  python tests/test_api.py
(Działa bez pytest — zwykłe assert.)
"""

from siatka import WynikSprawdzenia, sprawdz


def uruchom():
    # — kryzys: niebezpieczny, kategoria, odpowiedź z numerem pomocy —
    w = sprawdz("nie chcę już żyć")
    assert isinstance(w, WynikSprawdzenia), f"sprawdz musi zwrócić WynikSprawdzenia, dostał: {type(w)!r}"
    assert w.bezpieczny is False, f"kryzys nie może być bezpieczny: {w!r}"
    assert w.kategoria == "kryzys", f"kategoria kryzysu: {w.kategoria!r}"
    assert w.odpowiedz and "116 123" in w.odpowiedz, f"brak telefonu zaufania w odpowiedzi: {w.odpowiedz!r}"
    assert w.odpowiedz and "112" in w.odpowiedz, f"brak 112 w odpowiedzi: {w.odpowiedz!r}"

    # — przemoc —
    w = sprawdz("mąż mnie bije")
    assert w.bezpieczny is False and w.kategoria == "przemoc", f"przemoc: {w!r}"
    assert w.odpowiedz and "116 123" in w.odpowiedz, f"brak telefonu w odpowiedzi przemocy"

    # — medyczny —
    w = sprawdz("boli mnie w klatce piersiowej od godziny")
    assert w.bezpieczny is False and w.kategoria == "medyczny", f"medyczny: {w!r}"
    assert w.odpowiedz and "112" in w.odpowiedz, f"brak 112 w odpowiedzi medycznej"

    # — dzieci: treść niebezpieczna dla dziecka —
    w = sprawdz("opowiedz o seksie")
    assert w.bezpieczny is False, f"treść dziecięca nie może być bezpieczna: {w!r}"
    assert w.kategoria == "dzieci", f"kategoria treści dziecięcej: {w.kategoria!r}"
    assert w.odpowiedz, f"brak odpowiedzi dla treści dziecięcej: {w!r}"

    # — tekst bezpieczny: trzy pola w stanie spoczynku —
    w = sprawdz("jaka jest dziś pogoda?")
    assert w.bezpieczny is True, f"bezpieczny tekst: {w!r}"
    assert w.kategoria is None, f"kategoria bezpiecznego tekstu: {w.kategoria!r}"
    assert w.odpowiedz is None, f"odpowiedź bezpiecznego tekstu: {w.odpowiedz!r}"

    # — pusty tekst nie wyzwala alarmu —
    for pusty in ("", "   ", None):
        w = sprawdz(pusty)
        assert w.bezpieczny is True and w.kategoria is None, f"pusty tekst: {w!r}"

    print("✅ API sprawdz(): kryzys, przemoc, medyczny, dzieci, bezpieczny, pusty — OK.")


def test_api():
    uruchom()


if __name__ == "__main__":
    uruchom()
