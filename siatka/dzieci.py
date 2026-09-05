"""Ostrzejszy filtr tresci dla trybu dla dzieci.

Dziala na wejsciu (co pisze dziecko) i na wyjsciu (co odpowiada model).
Deterministyczny filtr slow; nie zastepuje nadzoru rodzica, ale wycina
oczywiste zle tematy. Nie zastepuje kontaktu z czlowiekiem.
"""

import re

class SiatkaDziecieca:
    # Wzorce niedozwolone (regex, z granicami słów tam, gdzie groziłyby pomyłki).
    WZORCE = [
        r"\bseks\w*", r"\bporno\w*", r"\bnag[ai]\b", r"\berotyk\w*",
        r"\bnarkotyk\w*", r"\bkokain\w*", r"\bmarihuan\w*", r"\b[ćc]pa\w*",
        r"\balkohol\w*", r"\bwódk\w*", r"\bwodk\w*", r"\bpiwo\b", r"\bpapieros\w*",
        r"\bzabi[ćcjł]\w*", r"\bzabij\w*", r"\bmorderstw\w*", r"\bzamordow\w*",
        r"\bpistolet\w*", r"\bkarabin\w*", r"\bbomb\w*", r"\bwojn\w*",
        r"\bsamob[oó]j\w*", r"\bgwałt\w*", r"\bgwalt\w*",
        r"\bkurw\w*", r"\bchuj\w*", r"\bpierdol\w*", r"\bjeb\w*", r"\bskurwy\w*",
        # — rozszerzenie po red-teamie —
        # używki / slang
        r"\bskręt\w*", r"\bjoint\w*", r"\btrawk\w*", r"\bzioło\b", r"\bblant\w*",
        r"\balko\b", r"\bwódeczk\w*", r"\bbrowar\w*", r"\bdrink\w*", r"\bupi[ćc]\w*",
        # wulgaryzmy
        r"\bspierdal\w*", r"\bzajeb\w*", r"\bpojeb\w*", r"\bdo dupy\b", r"\bdupek\w*",
        r"\bkurew\w*", r"\bgnoj\w*", r"\bdebil\w*", r"\bidiot\w*",
        # treści dla dorosłych
        r"\bgoł[aąeyo]\b", r"\bgolizn\w*", r"\bgolas\w*",   # nagość (bez "gołąb")
        r"\bdziewic\w*", r"\bpenis\w*", r"\bwagin\w*", r"\bcyc\w*",
        r"\bcałowa[ćc]\s+(?:się\s+)?z\s+językiem",
        # niebezpieczne instrukcje
        r"\bpodpali[ćc]\b", r"\bpodpal\w*", r"\bzrani[ćc]\b", r"\bukraś[ćc]\b", r"\bkraś[ćc]\b",
        r"\btrucizn\w*", r"\bzatru[ćc]\w*",
        # grooming / kontakt z obcym
        r"\bpodaj\s+(?:mi\s+)?(?:swój\s+)?adres",
        r"\bgdzie\s+mieszkasz",
        r"\b(?:twój|swój)\s+(?:adres|numer|telefon|hasło)",
        r"\bnie\s+mów\s+(?:o tym\s+)?(?:rodzic|mamie|tacie|nikomu)",
        r"\bto\s+nasz\s+sekret",
        r"\bspotkajmy\s+się",
        r"\bspotkaj\s+się\s+ze\s+mną",
        # kryzys dziecka
        r"\bnienawidz[eę]\s+siebie", r"\bnie\s+chc[eę]\s+ży[ćc]",
    ]

    def __init__(self):
        self._wzorce = [re.compile(w, re.IGNORECASE) for w in self.WZORCE]

    # Polskie jednoliterowe słowa — NIE wolno ich sklejać z sąsiadem, bo "o seksie"
    # nie może stać się "oseksie" (zgubilibyśmy granicę \b w "o s e k s i e").
    _JEDNOLITEROWE = {"a", "i", "o", "u", "w", "z"}

    def _sklej_litery(self, t: str) -> str:
        """Anty-bypass: dziecko rozbija słowo separatorami ("s e k s", "k.u.r.w.a"),
        by ominąć filtr. Sklejamy ciągi POJEDYNCZYCH liter; jednoliterowe słowa PL
        (o, w, i, a, u, z) i słowa dłuższe niż litera traktujemy jako granicę."""
        tokeny = re.sub(r"[.\-_*]+", " ", t).split()
        wynik, bufor = [], []
        for tok in tokeny:
            if len(tok) == 1 and tok.isalpha() and tok not in self._JEDNOLITEROWE:
                bufor.append(tok)
            else:
                if bufor:
                    wynik.append("".join(bufor)); bufor = []
                wynik.append(tok)
        if bufor:
            wynik.append("".join(bufor))
        return " ".join(wynik)

    def _sklej_zachlannie(self, t: str) -> str:
        """Wariant zachłanny: skleja KAŻDY ciąg pojedynczych liter, nawet gdy są to
        polskie słowa jednoliterowe (u, w, a) — bo "k u r w a" to też bypass.
        Komplementarny do _sklej_litery (które chroni granicę w "o s e k s i e")."""
        tokeny = re.sub(r"[.\-_*]+", " ", t).split()
        wynik, bufor = [], []
        for tok in tokeny:
            if len(tok) == 1 and tok.isalpha():
                bufor.append(tok)
            else:
                if bufor:
                    wynik.append("".join(bufor)); bufor = []
                wynik.append(tok)
        if bufor:
            wynik.append("".join(bufor))
        return " ".join(wynik)

    def niebezpieczne(self, tekst: str) -> bool:
        if not tekst:
            return False
        t = tekst.lower()
        warianty = (t, self._sklej_litery(t), self._sklej_zachlannie(t))
        return any(w.search(v) for w in self._wzorce for v in warianty)

    def przekierowanie(self) -> str:
        return ("Pobawmy się w coś fajnego! Chcesz zagadkę, grę w zgadywankę, "
                "albo nauczyć się nowego angielskiego słówka?")