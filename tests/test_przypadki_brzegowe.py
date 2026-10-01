"""Przypadki brzegowe: literówki, brak polskich znaków, zdania z przeczeniem.

Uruchom:  python tests/test_przypadki_brzegowe.py
(Działa bez pytest — zwykłe assert. Z pytest też przejdzie.)

Każda grupa ma dwie części:
  * co filtr MA robić — twarde asercje,
  * ZNANE LUKI — zdania, których filtr dziś NIE obsługuje tak, jak byśmy
    chcieli. Są zapisane jawnie, żeby granica była widoczna, a nie odkrywana
    przy wdrożeniu. Gdy któreś zacznie przechodzić, bo filtr się poprawił,
    test o tym powie — wtedy przenieś zdanie do listy „ma łapać".
"""

from siatka import sprawdz
from siatka.dzieci import SiatkaDziecieca
from siatka.kryzys import SiatkaBezpieczenstwa

S = SiatkaBezpieczenstwa()
D = SiatkaDziecieca()


def _sprawdz_luki(luki, faktycznie):
    """Znana luka ma dalej być luką — inaczej ktoś poprawił filtr i nie
    zaktualizował testów (albo zmienił zachowanie przez przypadek)."""
    for tekst, oczekiwane in luki:
        wynik = faktycznie(tekst)
        assert wynik == oczekiwane, (
            f"ZNANA LUKA ZMIENIŁA ZACHOWANIE: {tekst!r} -> {wynik!r} "
            f"(było {oczekiwane!r}). Jeśli to poprawa — przenieś zdanie do "
            "asercji twardych i opisz zmianę."
        )


# ── 1. Brak polskich znaków, wielkość liter, białe znaki ──────────────────────

def test_brak_polskich_znakow():
    """Filtr BLOKUJĄCY składa diakrytyki tekstu i wzorców do ASCII, więc
    „nie chce juz zyc" = „nie chcę już żyć". Pilnujemy tego dla każdej
    kategorii, a nie tylko dla jednego zdania z README."""
    pary = [
        # (bez ogonków, kategoria)
        ("nie chce juz zyc", "kryzys"),
        ("chce sie zabic", "kryzys"),
        ("mysle o samobojstwie", "kryzys"),
        ("nie chcialbym zyc", "kryzys"),
        ("chcialabym umrzec", "kryzys"),
        ("wolalbym sie nie obudzic", "kryzys"),
        ("nie widze sensu w zyciu", "kryzys"),
        ("jestem ciezarem dla wszystkich", "kryzys"),
        ("maz mnie bije", "przemoc"),
        ("maz mnie uderzyl", "przemoc"),
        ("boje sie meza", "przemoc"),
        ("grozi mi smiercia", "przemoc"),
        ("moj chlopak mnie dusi", "przemoc"),
        ("nie moge oddychac", "medyczny"),
        ("opadl mi kacik ust", "medyczny"),
    ]
    for tekst, kategoria in pary:
        assert S.sprawdz(tekst) == kategoria, f"BEZ OGONKÓW: {tekst!r} -> {S.sprawdz(tekst)!r}"

    # Mieszanka: część słów z ogonkami, część bez (typowe dla STT i telefonu).
    for tekst in ("nie chce juz życ", "nie chcę zyć", "nie myślę o samobojstwie"):
        assert S.sprawdz(tekst) == "kryzys", f"MIESZANE OGONKI: {tekst!r}"

    # Wielkie litery, także wielkie litery z ogonkami (Ę, Ż, Ć).
    for tekst in ("NIE CHCĘ JUŻ ŻYĆ", "NIE CHCE JUZ ZYC", "Nie Chce Juz Zyc"):
        assert S.sprawdz(tekst) == "kryzys", f"WIELKIE LITERY: {tekst!r}"

    # Warstwa wspierająca też działa bez ogonków.
    for tekst in ("nie dam rady dluzej", "nie ma po co wstawac", "jestem bezwartosciowy"):
        assert S.wsparcie(tekst) == "wsparcie", f"WSPARCIE BEZ OGONKÓW: {tekst!r}"

    # Pełne API: bez ogonków też dostajemy numer pomocy.
    w = sprawdz("nie chce juz zyc")
    assert w.kategoria == "kryzys" and "116 123" in w.odpowiedz


def test_biale_znaki_i_interpunkcja():
    musi_lapac = [
        "nie chcę już żyć!!!",
        "  nie chcę żyć  ",
        "nie chcę\nżyć",          # złamanie linii (np. wklejony tekst)
        "nie chce\tzyc",
        "chcę  się zabić",        # podwójna spacja w środku
    ]
    for tekst in musi_lapac:
        assert S.sprawdz(tekst) == "kryzys", f"BIAŁE ZNAKI: {tekst!r}"
    assert S.sprawdz("mąż  mnie bije") == "przemoc"

    # Dawne ZNANE LUKI, zamknięte normalizacją wejścia (`siatka.normalizacja`).
    # Wzorzec „nie " + _CHCE ma dosłowną spację, więc podwójna spacja albo
    # myślniki między „nie" a „chcę" omijały warstwę kryzysową, a zdanie wpadało
    # do filtra DZIECIĘCEGO — człowiek w kryzysie dostawał „Pobawmy się w coś
    # fajnego!" zamiast 116 123. Pilnujemy kategorii przez PEŁNE API, bo właśnie
    # zła kategoria była tu błędem, nie brak alarmu.
    must_catch = [
        "nie  chcę   żyć",
        "nie-chcę-żyć",
        "nie_chce_zyc",
        "nie.chce.zyc",
        "nie chcę\t\tjuż  żyć",
        "NIE - CHCĘ - ŻYĆ",
    ]
    for tekst in must_catch:
        w = sprawdz(tekst)
        assert w.kategoria == "kryzys", f"NORMALIZACJA: {tekst!r} -> {w.kategoria!r}"
        assert "116 123" in w.odpowiedz
    assert sprawdz("mąż - mnie - bije").kategoria == "przemoc"

    # Warstwa wspierająca: kropka na końcu i myślniki nie psują kotwicy końcowej.
    for tekst in ("nie dam rady dłużej.", "nie-dam-rady-dłużej", "nie obudzić się jutro."):
        assert S.wsparcie(tekst) == "wsparcie", f"WSPARCIE PO NORMALIZACJI: {tekst!r}"

    # ZNANA LUKA: przecinek NIE jest normalizowany celowo — „nie, chcę żyć"
    # znaczy coś przeciwnego niż „nie chcę żyć".
    _sprawdz_luki(
        [("nie chcę, żyć", None)],
        lambda t: sprawdz(t).kategoria,
    )


def test_tryb_dzieci_bez_polskich_znakow():
    """Filtr dziecięcy sprawdza tekst i wzorce w obu postaciach: z polskimi
    znakami i bez nich (tak jak warstwa kryzysowa)."""
    zablokuj = [
        "wodka", "gwalt", "zabic", "gdzie mieszkasz", "to nasz sekret",
        "NARKOTYKI", "Narkotyki", "SEKS", "seksss",
        # dawne ZNANE LUKI — wzorce zapisane tylko z ogonkami; wśród nich
        # grooming, który dziecko pisze bez ogonków równie często jak dorosły
        "nie mow rodzicom",
        "podaj mi swoj adres",
        "spotkajmy sie",
        "chce wodeczki",
        "zapalmy skreta",
        "nie chce zyc",
        "s-p-o-t-k-a-j-m-y sie",
    ]
    for tekst in zablokuj:
        assert D.niebezpieczne(tekst), f"DZIECI BEZ OGONKÓW: {tekst!r}"
    assert sprawdz("nie chce zyc").kategoria == "kryzys"

    # ZNANA LUKA, świadoma: „goł[aąeyo]" nie ma wersji bez ogonków, bo „gola"
    # to też „strzeliłem gola". Patrz SiatkaDziecieca._TYLKO_Z_OGONKAMI.
    _sprawdz_luki([("pokaz gola pania", False)], D.niebezpieczne)
    assert D.niebezpieczne("pokaż gołą panią")


def test_zdania_dziecka_bez_alarmu():
    """Fałszywe alarmy: zwykłe zdania dziecka (szkoła, zabawa, jedzenie) NIE
    mogą włączyć żadnej warstwy. Składanie diakrytyków w filtrze dziecięcym
    zwiększa ryzyko kolizji ze zwykłymi słowami — ten test je łapie.
    Część zdań celowo bez ogonków i z myślnikami, jak pisze dziecko."""
    zdania = [
        # szkoła
        "Dzisiaj w szkole mieliśmy klasówkę z matmy",
        "Pani od polskiego zadała wypracowanie",
        "mam jutro sprawdzian z przyrody",
        "Kolega pożyczył mi gumkę",
        "Kupiliśmy nowe buty do szkoły",
        "Ile jest dwa razy trzy?",
        "czytam ksiazke o dinozaurach",
        # zabawa
        "Strzeliłem gola na WF-ie",
        "strzelilem gola na wfie",
        "Na przerwie graliśmy w berka",
        "Idę z tatą na plac zabaw",
        "Zbudowałem wieżę z klocków Lego",
        "Zagrajmy w chowanego",
        "gramy w Minecrafta, zbudowalem dom",
        "Wczoraj padał deszcz i skakałem po kałużach",
        # jedzenie
        "Mama zrobiła naleśniki z dżemem",
        "Na obiad była zupa pomidorowa",
        "lubie lody czekoladowe",
        "Czy mogę zjeść jabłko?",
        "Zjadłem kanapkę z serem na drugie śniadanie",
    ]
    assert len(zdania) == 20
    for tekst in zdania:
        w = sprawdz(tekst)
        assert w.bezpieczny, f"FAŁSZYWY ALARM: {tekst!r} -> {w.kategoria!r}"
        assert S.wsparcie(tekst) is None, f"FAŁSZYWY ALARM WSPARCIA: {tekst!r}"

    # ZNANY FAŁSZYWY ALARM sprzed normalizacji (wzorzec `\bbomb\w*`), poza
    # zakresem tego PR — trafi do przeglądu wzorców dziecięcych.
    _sprawdz_luki(
        [("Ubieramy choinkę i wieszamy bombki", "dzieci")],
        lambda t: sprawdz(t).kategoria,
    )


# ── 2. Literówki ──────────────────────────────────────────────────────────────

def test_literowki():
    """Filtr opiera się na wzorcach, nie na odległości edycyjnej. Łapie
    literówki, które nie psują dopasowanego rdzenia (np. powtórzona litera
    na końcu słowa), a gubi te, które go psują."""
    musi_lapac = [
        ("nie chce żyćć", "kryzys"),       # powtórzona litera za rdzeniem
        ("nie chce zyć", "kryzys"),        # zgubiony jeden ogonek
        ("nie chcę życ", "kryzys"),
        ("zabiję sie", "kryzys"),
        ("mąż mnie bijeeee", "przemoc"),
    ]
    for tekst, kategoria in musi_lapac:
        assert S.sprawdz(tekst) == kategoria, f"LITERÓWKA: {tekst!r} -> {S.sprawdz(tekst)!r}"

    assert D.niebezpieczne("seksss")

    # ZNANE LUKI — literówka w samym rdzeniu wzorca. To ograniczenie podejścia
    # opartego na wzorcach, opisane w README (Limitations).
    _sprawdz_luki(
        [
            ("nie chcem żyć", None),
            ("nie hcę żyć", None),
            ("nie chcę już żyyyć", None),
            ("samobujstwo", None),               # ó → u (błąd ortograficzny)
            ("nie myśle o samobujstwie", None),
            ("chcę się zabć", None),
            ("chce sie zabiś", None),
            ("mąż mnie bję", None),
        ],
        S.sprawdz,
    )
    _sprawdz_luki(
        [("sex", False), ("s3ks", False), ("kurva", False)],
        D.niebezpieczne,
    )


# ── 3. Zdania z przeczeniem ───────────────────────────────────────────────────

def test_przeczenie_kryzys():
    """Przeczenie NIE wyłącza alarmu kryzysowego — to decyzja projektowa.

    Filtr nie rozumie składni, więc „nie myślę o samobójstwie" wygląda dla
    niego tak samo jak „myślę o samobójstwie". Świadomie wolimy fałszywy
    alarm niż przegapiony kryzys; ludzie w kryzysie często zaprzeczają
    („nie, nie zrobię sobie krzywdy") w tym samym zdaniu, w którym o tym mówią.
    """
    nadczule = [
        "nie myślę o samobójstwie",
        "nigdy nie myślałem o samobójstwie",
        "nie chcę się zabić",
        "nie zabiję się, spokojnie",
        "nie mam myśli samobójczych",
        "nie mam dość życia",
        "nie tnę się",
        "nie chcę zniknąć",
    ]
    for tekst in nadczule:
        assert S.sprawdz(tekst) == "kryzys", (
            f"ZMIANA GRANICY bez decyzji: przeczenie wyłączyło alarm dla {tekst!r}. "
            "Jeśli to celowe — opisz decyzję w kryzys.py i w README."
        )

    # Przeczenie, które jest częścią wzorca, działa zgodnie z sensem:
    # „nie chcę żyć" to kryzys, „chcę żyć" nie.
    for tekst in ("chcę żyć", "bardzo chcę żyć", "nie, chcę żyć", "nie jestem w kryzysie"):
        assert S.sprawdz(tekst) is None, f"FAŁSZYWY ALARM: {tekst!r} -> {S.sprawdz(tekst)!r}"


def test_przeczenie_przemoc_i_medyczne():
    """Dla przemocy i stanów medycznych przeczenie działa tylko wtedy, gdy
    rozrywa dopasowaną frazę („mąż mnie NIE bije"). Gdy stoi przed frazą,
    filtr i tak reaguje — spójnie z zasadą „lepiej raz za dużo"."""
    przepuszczone = [
        "mąż mnie nie bije",
        "nikt mi nie grozi",
        "nie mam udaru",
        "nie mam drgawek",
    ]
    for tekst in przepuszczone:
        assert S.sprawdz(tekst) is None, f"FAŁSZYWY ALARM: {tekst!r} -> {S.sprawdz(tekst)!r}"

    # Nadczułość zaakceptowana: przeczenie PRZED frazą nie wyłącza alarmu.
    _sprawdz_luki(
        [
            ("nie grozi mi nic", "przemoc"),
            ("nie boli mnie w klatce", "medyczny"),
            ("nie mam zawału", "medyczny"),
        ],
        S.sprawdz,
    )

    # Tryb dzieci: przeczenie nie zmienia tematu — rozmowa o seksie/alkoholu
    # jest poza trybem dziecięcym niezależnie od „nie".
    for tekst in ("nie mów o seksie", "nie lubię alkoholu", "nie zabijaj"):
        assert D.niebezpieczne(tekst), f"DZIECI + PRZECZENIE: {tekst!r}"


def uruchom():
    testy = [
        test_brak_polskich_znakow,
        test_biale_znaki_i_interpunkcja,
        test_tryb_dzieci_bez_polskich_znakow,
        test_zdania_dziecka_bez_alarmu,
        test_literowki,
        test_przeczenie_kryzys,
        test_przeczenie_przemoc_i_medyczne,
    ]
    for t in testy:
        t()
    print(f"✅ Przypadki brzegowe: {len(testy)} grup (ogonki, białe znaki, "
          "tryb dzieci, zdania dziecka, literówki, przeczenia) — OK, "
          "znane luki bez zmian.")


if __name__ == "__main__":
    uruchom()
