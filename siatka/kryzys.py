"""Deterministyczny filtr kryzysowy dla tekstu po polsku.

Wykrywa wypowiedzi o samobójstwie, przemocy i naglych stanach medycznych
w surowym tekscie — niezaleznie od modelu AI. To siatka bezpieczenstwa,
nie zastepuje pomocy specjalisty ani kontaktu z czlowiekiem.
"""

import re
from typing import Optional

class SiatkaBezpieczenstwa:
    # Frazy o wysokim ryzyku — odmieniane warianty. Celowo szerokie,
    # bo lepiej zareagować raz za dużo niż przegapić.
    # chc[eę]|chcia\u0142(?:a)?bym  obejmuje: chcę, chce, chciałbym, chciałabym
    # (?:\w+\s+){0,2} pozwala na słowa wypełniające ("już", "dalej", "po prostu")
    #
    # DLACZEGO {0,3} przy formie bezosobowej (poprawka 2026-08-05, test na żywo):
    # polska konstrukcja zwrotna wstawia DWA słowa ("mi się"), a do tego dochodzi
    # wzmacniacz ("już", "dalej", "w ogóle") — razem TRZY. Przy {0,2} zdanie
    # "nie chce mi się już żyć", czyli najzwyklejsze sformułowanie w tym języku,
    # mijało filtr o JEDNO słowo i szło prosto do modelu. Zmierzone na żywo:
    # model odpowiedział rozmową o herbacie z miętą, bez jednego numeru pomocy.
    # Szerszą lukę (_LUKA) dajemy TYLKO tam, gdzie kotwica mówi jednoznacznie
    # o sobie (żyć, istnieć, umrzeć, zniknąć); przy "zabić" zostaje {0,2}, bo tam
    # szerszy odstęp łapałby zdania o kimś innym.
    _CHCE = r"(?:chc[eę]|chcia\u0142(?:a)?bym|chcia\u0142(?:a)?em)"
    # Luka między "nie chcę" a czasownikiem: do CZTERECH słów wypełniających
    # ("mi się w ogóle"), ale ŻADNE z nich nie może być "żeby/aby/by". To jedno
    # słowo odwraca sens zdania z mówienia o sobie na mówienie o kimś innym:
    # "nie chcę, żeby mój syn musiał żyć w takim świecie" to troska rodzica,
    # nie sygnał kryzysu — a alarm w takim miejscu uczy człowieka ignorować filtr.
    _LUKA = r"\s+(?:(?!żeby|aby|by\s)\w+\s+){0,4}"
    FRAZY_KRYZYS = [
        r"nie " + _CHCE + _LUKA + r"\u017cy[\u0107c]",
        _CHCE + r"\s+(?:\w+\s+){0,2}zabi[\u0107c]",
        _CHCE + r"\s+(?:\w+\s+){0,3}umrze[\u0107c]",
        r"odebra[\u0107c]\s+sobie\s+\u017cycie",
        r"my\u015bl[ieę]\s+(?:\w+\s+){0,2}o\s+samob\u00f3jstwie",
        r"samob\u00f3jstw",
        r"zrobi[\u0107c]\s+sobie\s+krzywd[eę]",
        r"nie ma sensu\s+(?:\w+\s+){0,2}\u017cy[\u0107c]",
        r"lepiej\s*,?\s*(?:\w+\s+){0,3}mnie\s+nie\s+by\u0142o",
        r"nie " + _CHCE + _LUKA + r"istnie[\u0107c]",
        # Tryb przypuszczaj\u0105cy bez "chc\u0119": "wola\u0142bym nie istnie\u0107/nie \u017cy\u0107".
        r"(?:wola\u0142(?:a)?bym|lepiej\s+(?:by\s+)?by\u0142o)" + _LUKA + r"nie\s+(?:istnie[\u0107c]|\u017cy[\u0107c]|\u017cy\u0142[aeo]?)",
        # Pytanie o sens w\u0142asnego istnienia. Kotwiczone na KO\u0143CU zdania, bo
        # "po co ja \u017cyj\u0119" to sygna\u0142, a "po co ja \u017cyj\u0119 tak daleko od pracy"
        # to zwyk\u0142e narzekanie \u2014 r\u00f3\u017cni je w\u0142a\u015bnie to, czy zdanie tam si\u0119 ko\u0144czy.
        r"po\s+co\s+(?:\w+\s+){0,3}\u017cyj[e\u0119]\s*[.?!\u2026]*$",
        r"zako\u0144cz[y\u0107c]*\s+(?:\w+\s+){0,2}wszystko",
        r"mam do\u015b[\u0107c]\s+\u017cycia",
        _CHCE + r"\s+(?:\w+\s+){0,2}zako\u0144czy[\u0107c]",
        r"planuj[eę]\s+(?:\w+\s+){0,2}zabi[\u0107c]",
        r"\u017cycie nie ma sensu",
        r"wszystko\s+(?:\w+\s+){0,1}bez sensu",
        # \u2014 rozszerzenie po red-teamie: go\u0142e czasowniki, metody, eufemizmy \u2014
        r"zabi[\u0107c]\s+si[e\u0119]",                       # zabi\u0107 si\u0119 (bezokolicznik)
        r"zabij[e\u0119]?\s+si[e\u0119]",                          # zabij\u0119/zabije si\u0119
        r"si[e\u0119]\s+zabij[e\u0119]",                           # si\u0119 zabij\u0119
        r"\bpowiesi[\u0107c]\s+si[e\u0119]\b",
        r"\bsi[e\u0119]\s+powiesi[\u0107c]\b",
        r"podci[\u0105a][\u0107c]\s+(?:sobie\s+)?\u017cy\u0142y",
        r"podetn[e\u0119]\s+(?:sobie\s+)?\u017cy\u0142y",
        r"(?:skocz[e\u0119]|rzuc[e\u0119] si[e\u0119]|skoczy[\u0107c])\s+(?:\w+\s+){0,3}(?:z\s+mostu|pod\s+(?:poci[\u0105a]g|samoch[o\u00f3]d))",
        r"my\u015bli\s+samob[o\u00f3]jcz",              # my\u015bli samob\u00f3jcze
        r"my\u015bl[e\u0119]\s+(?:\w+\s+){0,3}(?:\u017ceby|by)\s+si[e\u0119]\s+zabi[\u0107c]",
        r"(?:mam zamiar|zamierzam|planuj[e\u0119])\s+(?:\w+\s+){0,2}(?:si[e\u0119]\s+)?(?:zabi[\u0107c]|sko\u0144czy[\u0107c] ze sob[\u0105a])",
        r"sko[\u0144n]czy[\u0107c]\s+ze\s+sob[\u0105a]",
        r"ze\s+sob[\u0105a]\s+sko[\u0144n]czy[\u0107c]",
        # red-team: stalo tu `chc[e]|wolalbym|pragne` — BEZ
        # `chcialbym`, choc stala _CHCE czterdziesci linii wyzej obejmuje wszystkie
        # trzy formy. Skutek: „chce zniknac" lapane, „chcialbym zniknac" przepuszczane.
        # Jedno brakujace slowo w alternatywie, cala klasa zdan na zewnatrz.
        r"(?:" + _CHCE + r"|wolał(?:a)?[bm]ym|wolal(?:a)?bym|pragn[eę])" + _LUKA + r"znikn[ąa][ćc]",
        r"znikn[\u0105a][\u0107c]\s+na\s+zawsze",
        r"odej[\u015bs][\u0107c]\s+na\s+zawsze",
        r"nie\s+chc[e\u0119]\s+(?:ju\u017c\s+|d\u0142u\u017cej\s+)?by[\u0107c]\b",
        r"nie\s+widz[e\u0119]\s+sensu\s+(?:w\s+)?\u017cyci",
        r"nie\s+chc[e\u0119]\s+si[e\u0119]\s+(?:ju\u017c\s+)?(?:obudzi[\u0107c]|budzi[\u0107c])",
        r"(?:wola\u0142[ab]ym|lepiej\s+jakbym|najlepiej\s+jakbym)\s+(?:si[e\u0119]\s+)?(?:\w+\s+){0,2}nie\s+(?:obudzi|budzi)[\u0142l\u0107c]",
        r"targn[\u0105a][\u0107c]\s+si[e\u0119]\s+na\s+(?:swoje\s+)?\u017cycie",
        r"(?:okalecz|tn[e\u0119]\s+si[e\u0119]|potn[e\u0119]\s+si[e\u0119])",  # samookaleczenie
        r"si[e\u0119]\s+okalecz",
        r"nienawidz[e\u0119]\s+(?:swojego\s+)?\u017cyci",
        r"nienawidz[e\u0119]\s+siebie",                       # nienawi\u015b\u0107 do siebie

        # ── BIERNA IDEACJA (27.08.2026) ─────────────────────────────────────
        # Znalezione POMIAREM, nie przeczuciem: model (rola audytora) uruchomiony
        # na samym kodzie tej klasy wypisal 12 zdan, ktorych filtr nie lapie.
        # Przeszlo 12/12. Cala lista wyzej celuje w mowe WPROST
        # („zabic sie", „samobojstwo", „nie chce zyc") i w metody — a czlowiek
        # w kryzysie najczesciej pisze NIE WPROST. To nie byla luka w jednym
        # wyrazeniu, tylko brakujaca KATEGORIA.
        #
        # Dokladamy WYLACZNIE zdania jednoznaczne. Swiadomie NIE dokladamy
        # „nie dam rady dluzej", „nie moge juz tak dalej", „jestem bezwartosciowy",
        # „nie ma po co wstawac" ani „zeby ten bol sie wreszcie skonczyl" — to samo
        # zdanie mowi czlowiek wykonczony praca albo chorym kregoslupem. Filtr,
        # ktory przerywa zwykla rozmowe numerem alarmowym, uczy go ignorowac.
        # Ta granica jest decyzja projektowa, nie kodu.

        # sen bez przebudzenia. Bylo tylko „nie chce sie obudzic" i „wolalbym sie
        # nie obudzic"; szyk „spac i nie budzic sie" mijal oba wzorce.
        r"(?:spa[ćc]|zasn[ąa][ćc])\s+(?:\w+\s+){0,3}nie\s+(?:budzi|obudzi)[ćcłl]",
        # poczucie bycia obciazeniem dla innych
        r"(?:jestem|czuj[eę]\s+si[eę])\s+(?:\w+\s+){0,2}ci[eę][żz]arem",
        # „wszystkim byloby lepiej beze mnie", „wszyscy byliby lepsi beze mnie"
        # Kotwiczone na formie „byc" ALBO na koncu wypowiedzi. Pierwsza wersja
        # (samo „lepiej beze mnie") zapalala sie na „lepiej beze mnie tego nie
        # zaczynajcie" — zlapal to wlasny test na falszywy alarm, nie uzytkownik.
        r"(?:by[łl]oby|byliby|by[łl]yby|b[eę]dzie|jest)\s+(?:\w+\s+){0,2}(?:lepiej|leps[iz]|lepsze)\s+beze\s+mnie",
        r"(?:lepiej|leps[iz]|lepsze)\s+beze\s+mnie\s*[.!?…]*$",
        # „nikt by nie plakal po mojej smierci" — kotwiczone na smierci/znikanie,
        # bo samo „nikt nie zauwazy" to zdanie o literowce, nie o zyciu
        r"nikt\s+(?:\w+\s+){0,4}(?:po\s+mojej\s+śmierci|jak\s+znikn[eę]|gdy\s+mnie\s+(?:już\s+)?nie\s+b[eę]dzie)",
        # zyczenie, zeby kolejny dzien nie nadszedl
        r"nie\s+" + _CHCE + r"\s+żeby\s+(?:jutro|jutrzejszy|ten\s+dzie[ńn]|kolejny\s+dzie[ńn])(?:\s+\w+){0,2}\s+(?:nadesz|nadejd|nasta|przysz)",
    ]

    # ── WARSTWA WSPIERAJACA — sygnal cierpienia, ktory NIE przerywa rozmowy ──
    #
    # POWOD (27.08.2026). Red-team wypisal 12 zdan, ktorych filtr nie
    # lapal. Szesc jednoznacznych dopisalismy wyzej do FRAZY_KRYZYS. Szesc zostalo
    # POZA nim swiadomie — bo to samo zdanie mowi czlowiek wykonczony praca albo
    # z chorym kregoslupem, a filtr przerywajacy zwykla rozmowe numerem alarmowym
    # uczy czlowieka ignorowac filtr.
    #
    # Druga opinia (27.08) przestawila pytanie i miala racje: problemem
    # nie bylo, GDZIE postawic granice, tylko ze mamy tylko DWA STANY — cisza albo
    # numer alarmowy. Te szesc zdan nie jest „troche kryzysowych"; one wymagaja
    # KONTEKSTU, ktorego wyrazenie regularne nie widzi, a rozmowa ma.
    #
    # ROZROZNIENIE, na ktorym stoi cala ta warstwa: kotwica na KONCU wypowiedzi.
    # „nie dam rady dluzej" to sygnal. „nie dam rady dluzej z tym projektem" to
    # zmeczenie — i konczy sie czym innym. Ten sam mechanizm, co przy „po co ja zyje"
    # w FRAZY_KRYZYS. Zmierzone na 20 zdaniach: 6 lapanych, 8 kontrolnych przepuszczonych.
    # ── Warstwa wspierajaca: ogon, wzmacniacze, rdzenie ──────────────────────
    # Rozszerzone PO POMIARZE na korpusie 88 zdan, nie po wyczuciu.
    # Stan przed zmiana: 7/39 zlapanych sygnalow, 2/36 falszywych alarmow.
    #
    # DLACZEGO LISTY ZAMKNIETE, A NIE "dowolne dwa slowa" - zmierzone:
    # ogon dowolny daje 4/36 falszywych, bo wpuszcza dopowiedzenia zmieniajace
    # sens na niewinny ("nie ma po co sie budzic PRZED ALARMEM", "czuje sie do
    # niczego PO TEJ GRYPIE"). Zdjecie kotwicy calkiem daje 22/36, czyli co
    # druga zwykla wypowiedz. Lista zamknieta: ten sam zysk, koszt bez zmian.

    # Dopowiedzenia czasu i stanu, ktore NIE wskazuja zewnetrznego zrodla zmeczenia.
    _OGON_WSP = (
        r"(?:\s*,?\s*(?:rano|dzisiaj|dzis|ostatnio|naprawde|juz|kompletnie|zupelnie"
        r"|od\s+(?:tygodnia|miesiaca|dawna|jakiegos\s+czasu|rana|wczoraj)"
        r"|w\s+ogole|w\s+tym\s+stanie|ani\s+dnia|z\s+tym\s+wszystkim"
        r"|w\s+tym\s+wszystkim|z\s+(?:tego\s+)?lozka"
        r"|jako\s+(?:ojciec|matka|maz|zona|czlowiek|rodzic)"
        r"|dalej|na\s+nic|z\s+tego|dla\s+nikogo|w\s+tym\s+domu|w\s+domu"
        r"|kazdego\s+(?:ranka|dnia)|nikomu))*\s*[.!?…,]*$"
    )
    # Wzmacniacze w DOWOLNEJ kolejnosci ("sie juz wreszcie"), tez lista zamknieta:
    # wersja przez (?:\w+\s+){0,3} dawala ten sam zysk i DOKLADALA falszywy alarm
    # na "Zeby to zebranie wreszcie sie skonczylo".
    _WZM_WSP = r"(?:\s+(?:sie|juz|wreszcie|nareszcie|w\s+koncu))*"

    FRAZY_WSPARCIA = [
        # ── rdzenie sprzed 28.08, teraz z ogonem zamiast twardej kotwicy ──
        r"nie\s+(?:moge|dam\s+rady|wytrzymam|wytrzymac)\s+(?:juz\s+)?(?:tego\s+)?(?:tak\s+)?(?:dalej|dluzej)" + _OGON_WSP,
        r"nie\s+ma\s+po\s+co\s+(?:wstawac|sie\s+budzic)" + _OGON_WSP,
        r"(?:jestem|czuje\s+sie)\s+(?:\w+\s+){0,2}bezwartosciow\w*" + _OGON_WSP,
        r"(?:jestem|czuje\s+sie)\s+(?:\w+\s+){0,2}do\s+niczego" + _OGON_WSP,
        r"zeby\s+(?:ten\s+)?bol" + _WZM_WSP + r"\s+(?:skonczy|mina)\w*" + _OGON_WSP,
        r"zeby\s+to" + _WZM_WSP + r"\s+skonczylo" + _OGON_WSP,

        # ── nowe kategorie cierpienia: granice cierpienia ─────────────────────
        # To NIE sa nowe formy starych fraz, tylko stany, ktorych warstwa
        # wczesniej nie probowala nazwac:
        # wyczerpanie, anhedonia, brak wyjscia, poczucie bycia ciezarem.
        r"nie\s+mam\s+(?:juz\s+)?sily" + _OGON_WSP,
        r"dluzej\s+(?:juz\s+)?(?:tak\s+)?nie\s+(?:moge|dam\s+rady|wytrzymam)" + _OGON_WSP,
        r"nie\s+ma\s+sensu\s+(?:wstawac|sie\s+budzic)" + _OGON_WSP,
        r"nic\s+mnie\s+(?:juz\s+)?nie\s+(?:cieszy|bawi|interesuje)" + _OGON_WSP,
        r"nie\s+widze\s+(?:z\s+tego\s+)?(?:zadnego\s+)?wyjscia" + _OGON_WSP,
        r"(?:nic\s+nie\s+jestem\s+wart\w*|do\s+niczego\s+sie\s+nie\s+nadaje\w*)" + _OGON_WSP,
        r"(?:tylko\s+)?(?:przeszkadzam|zawadzam)\s+(?:tu\s+)?(?:tylko\s+)?(?:wszystkim|w\s+tym\s+domu|w\s+domu)" + _OGON_WSP,
        r"nie\s+dam\s+rady\s+(?:juz\s+)?(?:dluzej\s+)?(?:tak\s+)?(?:dalej\s+)?zyc" + _OGON_WSP,
        r"po\s+co\s+ja\s+(?:w\s+ogole\s+)?(?:jeszcze\s+)?wstaje" + _OGON_WSP,
        r"nie\s+moge\s+(?:juz\s+)?(?:tak\s+)?dalej\s+(?:funkcjonowac|zyc|isc)" + _OGON_WSP,
        # "bezwartosciowy" bez kotwicy koncowej, ale Z PODMIOTEM w pierwszej osobie.
        # Audyt proponowal wzorzec bez podmiotu; zawezilem go swiadomie, bo samo
        # slowo pada tez o rzeczach ("ten kurs byl bezwartosciowy"), a tego
        # przypadku w korpusie nie bylo - brak dowodu to nie dowod braku.
        r"(?:jestem|czuje\s+sie|robie\s+sie)\s+(?:\w+\s+){0,3}bezwartosciow\w*",
        # dolozone po pierwszym przebiegu 28.08: trzy formy, ktore korpus pokazal,
        # a wzorce ich nie obejmowaly. Kazda sprawdzona osobno na grupie B.
        r"nie\s+widze\s+po\s+co\s+(?:mam\s+)?(?:wstawac|zyc)" + _OGON_WSP,
        r"nic\s+ze\s+mnie\s+nie\s+ma\s+pozytku" + _OGON_WSP,
        r"zaluje\s*,?\s*ze\s+sie\s+(?:obudzil|w\s+ogole\s+obudzil)\w*" + _OGON_WSP,

        # ── BEZOKOLICZNIK BEZ PODMIOTU, czyli ogon pocietego zdania ───────────
        # Powod policzalny: rozpoznawanie mowy tnie wypowiedz na zdania.
        # Ze zdania "chcialbym zniknac i nie
        # obudzic sie jutro" pierwsza polowa trafia do FRAZY_KRYZYS, a druga — "i nie
        # obudzic sie jutro" — nie pasowala do NICZEGO, bo wszystkie dotychczasowe wzorce
        # snu bez przebudzenia wymagaja czasownika chcenia ("nie chce sie obudzic",
        # "wolalbym sie nie obudzic", "spac i nie budzic sie"). Zmierzone na zywo:
        # model odpowiadal na ten fragment "zapisane 😊" albo poprawial uzytkownikowi zdanie.
        #
        # DLACZEGO TU, A NIE W FRAZY_KRYZYS: sam bezokolicznik bez kontekstu nie jest
        # jednoznacznym kryzysem, a "obudzic sie jutro" pada w domu codziennie. Twarde
        # przerwanie rozmowy numerem alarmowym uczy czlowieka ignorowac filtr.
        #
        # KOTWICA NA KONCU JEST TU OBOWIAZKOWA, nie ozdobna: "nie obudzic sie jutro
        # o piatej" to zdanie o budziku i MUSI przejsc. Dlatego zamiast _OGON_WSP
        # (ktory dopuszcza dopowiedzenia) stoi twardy koniec wypowiedzi.
        r"nie\s+(?:obudzic|budzic)\s+sie\s+(?:jutro|wiecej|juz\s+nigdy|nigdy\s+wiecej)\s*[.!?…]*$",
        r"(?:jutro|wiecej)\s+sie\s+nie\s+(?:obudzic|budzic)\s*[.!?…]*$",
    ]

    # ── Bezpiecznik ramy cudzej mowy ──────────────────────────────────────────
    # ZMNIEJSZA liczbe falszywych alarmow: "Napisz wiersz, w ktorym ktos mowi, ze
    # nie ma po co wstawac" dostawalo zdanie troski. Wersja SZEROKA zostala
    # odrzucona po pomiarze, bo blokowala WLASNE wypowiedzi uzytkownika
    # ("Mowie Ci szczerze, nie dam rady dalej") - stad \b i (?<!nie\s).
    # Bezpiecznik ma nie kasowac sygnalu tylko dlatego, ze pada czasownik mowienia.
    FRAZY_RAMA_CUDZEJ_MOWY = [
        r"^\s*(?:napisz|uloz|wymysl|wygeneruj|opowiedz)\b",
        r"\b(?<!nie\s)(?:mowi|mowil|mowila|powiedzial|powiedziala|napisal|napisala)\b\s*[,:]?\s*(?:ze\b|,|:)",
        r"\bw\s+(?:filmie|ksiazce|piosence|serialu)\b",
        r"\bcytat\w*",
        r"\bbohater\w*",
    ]


    # Frazy o przemocy
    FRAZY_PRZEMOC = [
        r"\bbije mnie\b",
        r"mnie bije",
        r"on(?:a)?\s+mnie\s+(?:\w+\s+){0,2}bije",
        r"boj[eę] si[eę]\s+(?:\w+\s+){0,3}(?:m[eę]\u017ca|\u017cony|partner)",
        r"grozi mi",
        # — rozszerzenie po red-teamie: sprawca→ofiara, groźby, duszenie —
        r"\bmnie\s+(?:\w+\s+){0,2}(?:uderzy[łl]|pobi[łl]|krzywdzi|dusi|szarpie)",
        r"\b(?:m[ąa][żz]|partner|chłopak|on)\s+(?:\w+\s+){0,3}mnie\s+(?:bije|krzywdzi|dusi|uderzy)",
        r"grozi\s+mi\s+(?:\w+\s+){0,2}(?:śmierci[ąa]|zabiciem)",
        r"boj[eę] si[eę]\s+(?:\w+\s+){0,3}(?:że\s+)?mnie\s+(?:zabije|skrzywdzi|zarobi)",
        r"chc[eę]\s+(?:go|j[ąa])\s+(?:\w+\s+){0,2}skrzywdzi[\u0107c]",
    ]

    # Nagłe stany medyczne — dopisane po teście na żywo. Na „boli mnie
    # w klatce piersiowej od godziny" filtr milczał, a model odsyłał do lekarza
    # pierwszego kontaktu. Przy objawach czerwonej flagi liczy się 112, nie wizyta.
    # Lista jest CELOWO WĄSKA: łapiemy objawy alarmowe, nie każdy ból. „Boli mnie
    # głowa", „boli mnie brzuch", „boli mnie ząb" mają przechodzić bez zatrzymania —
    # filtr, który krzyczy przy katarze, przestaje być traktowany serio.
    FRAZY_MEDYCZNE = [
        # kardiologiczne
        r"b[oó]l\w*\s+(?:\w+\s+){0,2}(?:w\s+)?klatce",
        r"boli\s+(?:\w+\s+){0,2}(?:w\s+)?klatce",
        r"(?:ucisk|piecze|gniecie)\s+(?:\w+\s+){0,2}(?:w\s+)?klatce",
        r"\bzawa[lł]\w*",
        # oddechowe — bez „duszę się", bo bywa przenośnią („duszę się w tej pracy")
        r"nie\s+mog[eę]\s+(?:\w+\s+){0,2}oddycha[ćc]",
        r"nie\s+mog[eę]\s+(?:\w+\s+){0,2}z[lł]apa[ćc]\s+tchu",
        r"brakuje\s+mi\s+(?:\w+\s+){0,1}(?:tchu|powietrza)",
        # udarowe — „udar słoneczny" wyłączony, bo to inna sytuacja i inne tempo
        r"\budar\b(?!\s+s[lł]oneczn)",
        r"opad[lł]\w*\s+(?:\w+\s+){0,2}(?:k[ąa]cik|usta|twarz)",
        r"dr[eę]twiej\w*\s+(?:\w+\s+){0,2}(?:r[eę]k|nog|twarz|po[lł]ow)",
        r"nie\s+mog[eę]\s+(?:\w+\s+){0,2}m[oó]wi[ćc]",
        # utrata przytomności / drgawki
        r"(?:straci[lł]\w*|traci)\s+(?:\w+\s+){0,2}przytomno[śs][ćc]",
        r"nie\s+(?:oddycha|reaguje)\b",
        r"\bdrgawk\w*",
        r"\bnieprzytomn\w*",
        # krwotok / zatrucie / anafilaksja
        r"\bkrwotok\w*",
        r"nie\s+(?:mog[eę]\s+)?(?:zatamowa[ćc]|zatrzyma[ćc])\s+(?:\w+\s+){0,2}krwi",
        # połknął / połknęła / połknęło — odmiana przez rodzaj, więc szeroki rdzeń
        r"(?:po[lł]kn\w*|wypi[lł]\w*)\s+(?:\w+\s+){0,3}(?:tabletk|chemi|[śs]rodek|p[lł]yn|trucizn)",
        r"\bzatru[lł]\w*\s+si[eę]",
        r"(?:spuch[lł]|opuch[lł])\w*\s+(?:\w+\s+){0,2}(?:j[eę]zyk|gard[lł]o|twarz)",
    ]

    TELEFON_ZAUFANIA = "116 123"  # Telefon Zaufania dla Dorosłych w Kryzysie (PL)
    TELEFON_DZIECI   = "116 111"  # Telefon Zaufania dla Dzieci i Młodzieży (PL)
    ALARMOWY         = "112"

    # ZAPIS DO WYMOWY — komunikat idzie teraz także GŁOSEM.
    # Powód policzalny: przy pierwszym teście głosowym syntezator
    # przeczytał „116 123" jako LICZBĘ — „sto szesnaście tysięcy sto dwadzieścia
    # trzy". Numer, którego nie da się wystukać ze słuchu, jest w kryzysie wart
    # tyle co brak numeru. Dopisujemy formę mówioną OBOK cyfr, a nie zamiast nich:
    # na ekranie mają zostać cyfry, bo z ekranu numer się przepisuje.
    # 112 zostaje bez dopisku — „sto dwanaście" to sposób, w jaki ten numer
    # naprawdę się w Polsce wymawia, więc syntezator czyta go poprawnie.
    TELEFON_ZAUFANIA_MOWA = "jeden jeden sześć, jeden dwa trzy"
    TELEFON_DZIECI_MOWA   = "jeden jeden sześć, jeden jeden jeden"

    # Składanie polskich diakrytyków → ASCII. Filtr ma być nadczuły: osoba
    # w kryzysie (albo STT) często pisze bez ogonków ("nie chce juz zyc").
    # Dopasowujemy WZORCE i TEKST w tej samej, złożonej formie, więc łapiemy
    # oba warianty bez dublowania listy fraz. Polskie znaki nie są metaznakami
    # regexa, więc składanie wzorca jest bezpieczne (ż→z, [żc]→[zc] itd.).
    _DIAKRYTYKI = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")

    @classmethod
    def _zloz(cls, tekst: str) -> str:
        """Składa diakrytyki TEKSTU użytkownika (tylko literalne znaki)."""
        return tekst.translate(cls._DIAKRYTYKI)

    @classmethod
    def _zloz_wzor(cls, wzor: str) -> str:
        """Składa diakrytyki WZORCA. Wzorce zawierają escape'y \\uXXXX jako
        literalne ciągi (raw-string) — translate ich nie ruszy, więc najpierw
        zamieniamy \\uXXXX na realne znaki (nie tykając \\s, \\w, \\b),
        a potem składamy wszystkie diakrytyki."""
        wzor = re.sub(r"\\u([0-9a-fA-F]{4})",
                      lambda m: chr(int(m.group(1), 16)), wzor)
        return wzor.translate(cls._DIAKRYTYKI)

    def __init__(self):
        self._wzorce_kryzys = [re.compile(self._zloz_wzor(w), re.IGNORECASE)
                               for w in self.FRAZY_KRYZYS]
        self._wzorce_przemoc = [re.compile(self._zloz_wzor(w), re.IGNORECASE)
                                for w in self.FRAZY_PRZEMOC]
        self._wzorce_medyczne = [re.compile(self._zloz_wzor(w), re.IGNORECASE)
                                 for w in self.FRAZY_MEDYCZNE]
        self._wzorce_wsparcia = [re.compile(self._zloz_wzor(w), re.IGNORECASE)
                                 for w in self.FRAZY_WSPARCIA]
        self._wzorce_rama = [re.compile(self._zloz_wzor(w), re.IGNORECASE)
                             for w in self.FRAZY_RAMA_CUDZEJ_MOWY]

    def sprawdz(self, tekst: str) -> Optional[str]:
        """
        Zwraca typ zagrożenia ('kryzys' / 'przemoc') albo None.
        Działa na surowym tekście — niezależnie od modelu AI. Odporny na brak
        polskich ogonków (tekst i wzorce porównujemy w formie bez diakrytyków).
        """
        if not tekst or not tekst.strip():
            return None
        t = self._zloz(tekst.lower())
        for wz in self._wzorce_kryzys:
            if wz.search(t):
                return "kryzys"
        for wz in self._wzorce_przemoc:
            if wz.search(t):
                return "przemoc"
        # Medyczne SPRAWDZAMY NA KOŃCU: gdy ktoś pisze naraz o bólu i o tym, że nie
        # chce żyć, pierwszeństwo ma kryzys — tam liczy się rozmowa, nie karetka.
        for wz in self._wzorce_medyczne:
            if wz.search(t):
                return "medyczny"
        return None

    def wsparcie(self, tekst: str) -> Optional[str]:
        """Sygnal cierpienia, ktory NIE przerywa rozmowy. Zwraca 'wsparcie' albo None.

        DLACZEGO TO OSOBNA METODA, a nie nowa wartosc z `sprawdz()`:
        wywolujacy `sprawdz()` robia `if typ:` i ZATRZYMUJA rozmowe. Dopisanie tu
        nowej wartosci zamienilo by troske w przerwanie rozmowy na czterech
        sciezkach naraz, po cichu i bez zmiany ani jednej linii u wywolujacych.
        Kontrakt `sprawdz()` zostaje nietkniety — nowe zachowanie kazda sciezka
        wlacza sobie JAWNIE.

        Pierwszenstwo: gdy tekst jest jednoczesnie kryzysem, `sprawdz()` i tak
        zadziala wczesniej u wywolujacego. Ta metoda sama tez to sprawdza, zeby
        nie dalo sie jej uzyc w oderwaniu i dostac lagodnej reakcji na „chce sie
        zabic".
        """
        if not tekst or not tekst.strip():
            return None
        if self.sprawdz(tekst):
            return None                  # kryzys/przemoc/medyczny ma pierwszenstwo
        t = self._zloz(tekst.lower())
        # Rama cudzej mowy: "napisz wiersz, w ktorym ktos mowi, ze nie ma po co
        # wstawac" to prosba o tekst, nie sygnal o czlowieku. Bezpiecznik stoi
        # PRZED wzorcami, bo ma je unieważnić, a nie z nimi konkurowac.
        # Dotyczy WYLACZNIE warstwy wspierajacej - `sprawdz()` (kryzys, przemoc)
        # celowo NIE ma tego wyjatku: tam koszt pomylki jest nieodwracalny
        # i wolimy zareagowac raz za duzo na cudza wypowiedz niz raz za malo.
        for wz in self._wzorce_rama:
            if wz.search(t):
                return None
        for wz in self._wzorce_wsparcia:
            if wz.search(t):
                return "wsparcie"
        return None

    def komunikat_wsparcia(self) -> str:
        """Jedno zdanie troski, jedno pytanie otwarte, jedno odeslanie do czlowieka.

        Czego tu NIE MA i to jest celowe: numerow alarmowych (te naleza do reakcji,
        ktora PRZERYWA rozmowe) oraz drugiego pytania. Warstwa ma prawo zapytac raz
        i wrocic do bycia asystentem — inaczej zaczyna udawac terapeute, a tego
        nie wolno nikomu tutaj.
        """
        return (
            "Zatrzymam się na chwilę, bo to zabrzmiało ciężko.\n\n"
            "Chcesz o tym powiedzieć coś więcej, czy wolisz, żebym pomógł z konkretną "
            "rzeczą, która Cię dziś przytłacza?\n\n"
            "Jeśli to trwa dłużej — powiedz o tym komuś bliskiemu. To naprawdę pomaga "
            "bardziej niż rozmowa ze mną."
        )

    def komunikat_wsparcia_dzieci(self) -> str:
        """To samo dla dziecka: prosciej i z odeslaniem do DOROSLEGO w domu,
        nie do telefonu zaufania — bo to nie jest reakcja kryzysowa."""
        return (
            "Zatrzymam się, bo to zabrzmiało smutno.\n\n"
            "Chcesz mi o tym opowiedzieć?\n\n"
            "I powiedz o tym mamie albo tacie — oni pomogą lepiej niż ja."
        )


    def komunikat(self, typ: str) -> str:
        """Komunikat bezpieczeństwa — zawsze kieruje do realnej pomocy."""
        if typ == "kryzys":
            return (
                "Słyszę, że jest Ci teraz naprawdę ciężko, i martwię się o Ciebie. "
                "Nie jestem w stanie zastąpić człowieka, a w takiej chwili ważne jest, "
                "żebyś porozmawiał z kimś, kto może realnie pomóc.\n\n"
                f"• Telefon zaufania (całodobowy, bezpłatny): {self.TELEFON_ZAUFANIA}"
                f" — czyli {self.TELEFON_ZAUFANIA_MOWA}\n"
                f"• W nagłej sytuacji zadzwoń: {self.ALARMOWY}\n\n"
                "Jeśli możesz — odezwij się też do kogoś bliskiego i nie zostawaj teraz sam. "
                "Jestem tutaj i chętnie z Tobą zostanę."
            )
        if typ == "medyczny":
            return (
                "To, co opisujesz, może być stanem nagłym. Nie jestem w stanie tego ocenić "
                "i nie chcę, żebyś tracił teraz czas na pisanie ze mną.\n\n"
                f"• Zadzwoń pod {self.ALARMOWY} albo bezpośrednio po pogotowie: 999\n"
                "• Jeśli objawy się nasilają albo ktoś traci przytomność — dzwoń natychmiast\n\n"
                "Nie czekaj, aż samo przejdzie, i nie zostawaj z tym sam. "
                "Lepiej zadzwonić niepotrzebnie niż za późno."
            )
        if typ == "przemoc":
            return (
                "To, co opisujesz, brzmi poważnie i Twoje bezpieczeństwo jest najważniejsze. "
                "Nie jestem w stanie pomóc w takiej sytuacji tak, jak zrobi to człowiek.\n\n"
                f"• Telefon zaufania: {self.TELEFON_ZAUFANIA} — czyli {self.TELEFON_ZAUFANIA_MOWA}\n"
                f"• Niebieska Linia (przemoc): 800 120 002\n"
                f"• W nagłym zagrożeniu zadzwoń: {self.ALARMOWY}\n\n"
                "Jeśli czujesz się zagrożony, rozważ kontakt z kimś, komu ufasz."
            )
        return ""

    def komunikat_dzieci(self, typ: str) -> str:
        """Wariant komunikatu dla TRYBU DZIECI — prosty język + telefon dla
        dzieci (116 111). Kryzys/przemoc u dziecka ma priorytet nad zabawą."""
        if typ == "medyczny":
            return (
                "To brzmi poważnie. Natychmiast powiedz o tym dorosłemu, który jest blisko — "
                "mamie, tacie albo komukolwiek dorosłemu.\n\n"
                f"Jeśli nikogo nie ma obok, zadzwoń {self.ALARMOWY}. To nic nie kosztuje.\n\n"
                "Nie czekaj i nie bój się zadzwonić."
            )
        if typ in ("kryzys", "przemoc"):
            return (
                "Słyszę, że jest Ci teraz bardzo ciężko, i to ważne. "
                "Koniecznie powiedz o tym dorosłemu, któremu ufasz — mamie, tacie, "
                "albo pani w szkole.\n\n"
                f"Możesz też zadzwonić, to nic nie kosztuje: {self.TELEFON_DZIECI} "
                f"— czyli {self.TELEFON_DZIECI_MOWA} "
                "(Telefon Zaufania dla Dzieci).\n"
                f"Gdy dzieje się coś groźnego od razu — zadzwoń {self.ALARMOWY}.\n\n"
                "Nie jesteś sam. Są ludzie, którzy chcą Ci pomóc."
            )
        return ""
