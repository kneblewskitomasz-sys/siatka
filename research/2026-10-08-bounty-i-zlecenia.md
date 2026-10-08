# Płatne zadania za kod, bounty, granty i zlecenia — stan na 2026-10-08

Odczyt wszystkich stron: **2026-10-08**. Do tabeli trafiły tylko pozycje, których **status sprawdziłem na stronie źródłowej** tego dnia.

## Co dało się sprawdzić

| Źródło | Wynik |
|---|---|
| GitHub (wyszukiwarka issues, strony issues/PR) | **sprawdzone** — jedyne źródło dostępne z tego środowiska |
| Algora.io, IssueHunt, Gitcoin, comma.ai/bounties, arkusz bounty tinygrad (Google Sheets), Useme, Oferia, hacknation.pl, NLnet | **niesprawdzone** — domeny nie rozwiązywały się z DNS albo były zablokowane. Zgodnie z regułą „bez aktualnej strony = pomiń” nie ma ich w tabeli. |
| Hugging Face | brak programu płatnych bounty (nie znalazłem) i domena zablokowana |

**Ograniczenie:** bez logowania GitHub nie pokazuje komentarzy, więc **liczba zgłoszeń („/attempt”, „/opire try”) jest zwykle nieznana**. Podaję tylko to, co widać: otwarte PR-y i przypisania.

## Tabela (sprawdzone na GitHubie 2026-10-08)

| # | Pozycja | Nagroda | Termin | Zgłoszenia / konkurencja | Wymagania | Dlaczego pasuje | Ryzyko |
|---|---|---|---|---|---|---|---|
| 1 | [Spectral-Finance/lux #99 — LLM Provider Abstraction Layer](https://github.com/Spectral-Finance/lux/issues/99) | **$600** (etykieta bounty, platforma niepodana) | brak | otwarte od 25.02.2025, nieprzypisane; jest konkurencyjny [PR #847](https://github.com/Spectral-Finance/lux/pull/847) z 25.06.2026, **bez żadnej recenzji** | uniwersalny interfejs dostawców, automatyczny wybór modelu, fallback, monitoring kosztu i wydajności, cache, dokumentacja | **router modeli i fallback** = nasz rdzeń kompetencji | opiekunowie nie recenzują od ponad 3 miesięcy; autor PR-a podał adresy portfeli kryptowalut, a sposób wypłaty jest niejasny |
| 2 | [claude-builders-bounty #4 — sub-agent recenzujący PR](https://github.com/claude-builders-bounty/claude-builders-bounty/issues/4) | **$150** przez Opire, „wypłata automatycznie po merge” | brak | otwarte od 27.03.2026; w wynikach wyszukiwania widać ok. 1584 interakcji, więc konkurencja jest bardzo duża | CLI albo GitHub Action, wynik w Markdown (streszczenie, ryzyka, sugestie, pewność), testy na 2 prawdziwych PR-ach, README | **bramki jakości i testy skutków** — robimy to na co dzień | wygrywa tylko scalony PR; ryzyko pracy na darmo |
| 3 | [onyx-dot-app/onyx #2281 — konektor Jira Service Management](https://github.com/onyx-dot-app/onyx/issues/2281) | etykieta „💎 Bounty” (Algora), **kwota niewidoczna** | brak | otwarte od 30.08.2024; widoczny PR #11722; ok. 150 komentarzy | konektor do platformy RAG (Python) | **RAG** — konektory źródeł danych | stare i zatłoczone; kwoty nie da się potwierdzić bez Algory |
| 4 | [BasedHardware/omi #18563 — przepis upsert do ChromaDB](https://github.com/BasedHardware/omi/issues/18563) | **$25 — tylko zaproponowane**, niezatwierdzone | brak | otwarte 24.09.2026; autor propozycji ma już [PR #18562](https://github.com/BasedHardware/omi/pull/18562); priorytet p3 „Someday” | skrypt tylko na bibliotece standardowej, dokumentacja, 3 testy | **ChromaDB** dokładnie w naszym stosie | znikoma kwota, praktycznie zajęte przez autora propozycji |
| 5 | [tenstorrent/tt-metal #8621 — Host Tilizer BFP8/4/2](https://github.com/tenstorrent/tt-metal/issues/8621) | **$500**, [regulamin programu](https://docs.tenstorrent.com/bounty_terms.html) | brak (otwarte od 17.05.2024) | nieprzypisane; 18 komentarzy | optymalizacja C++ po stronie hosta | wiarygodny płatnik; praca na CPU | **słabe dopasowanie** (C++/HPC, nie nasz profil) |

**Odrzucone mimo statusu „open” (sprawdzone):**
- [tenstorrent/tt-metal #59732](https://github.com/tenstorrent/tt-metal/issues/59732) ($3000, otwarte 07.10.2026): już przypisane, PR złożony, wymaga sprzętu Tenstorrent (Wormhole/Blackhole).
- [tinygrad #18310](https://github.com/tinygrad/tinygrad/issues/18310) (emulator QCOM A630): poza profilem.
- **Farmy „bounty”** (SecureBananaLabs/bug-bounty, Scottcjn/rustchain-bounties z nagrodami w tokenach RTC, zhangjiayang6835-cyber/bounty-plaza z repostami cudzych bounty, UnsafeLabs „AI only allowed”). **WNIOSEK:** setki zgłoszeń, nagrody w tokenach albo reposty bez gwarancji wypłaty; wysokie ryzyko oszustwa. Pomijać.

## TOP 5 z rekomendacją

1. **lux #99 ($600)**: robić **tylko po** zadaniu opiekunom pytania na issue, czy recenzują i jak płacą. Jeśli odpowiedzą w ciągu 7 dni, zgłosić propozycję. Nasza przewaga: router z bramkami jakości i testami, a nie sam interfejs.
2. **claude-builders-bounty #4 ($150)**: ograniczyć pracę do ok. 4 h. Zrobić jako produkt uboczny naszego własnego recenzenta PR-ów; nawet bez wygranej narzędzie zostaje u nas.
3. **onyx #2281**: najpierw sprawdzić kwotę i stan zgłoszeń na Algorze ręcznie. Bez tego nie zaczynać.
4. **omi #18563 ($25)**: nie robić. Zajęte i symboliczne.
5. **tt-metal #8621 ($500)**: nie robić. Wiarygodny płatnik, ale poza profilem.

**Rekomendacja ogólna (WNIOSEK):** na GitHubie nie ma dziś świeżych, wiarygodnych bounty dopasowanych do profilu „lokalny asystent PL + dane publiczne PL + AMD”. Czas lepiej włożyć w źródła z listy poniżej.

## Do ręcznej weryfikacji (nie sprawdzone na stronie źródłowej — poza tabelą)

| Pozycja | Co mówią źródła wtórne | Gdzie sprawdzić |
|---|---|---|
| NLnet Restack | nabór do **03.11.2026 12:00 CET**, 5–50 tys. € (wyszukiwarka, 2026-09-30) | https://nlnet.nl/news/2026/20260903-call.html |
| Ścieżka SMART (PARP, pojedyncze MŚP) | nabór **29.10–29.12.2026**; wymaga firmy | https://www.parp.gov.pl/harmonogram-naborow |
| HackNation 2026 (Ministerstwo Cyfryzacji / GovTech) | **21–22.11.2026**, Bydgoszcz, 17 wyzwań, udział bezpłatny | https://hacknation.pl/ |
| Warsaw Open Data Hackathon | 17–18.10.2026, pula 18 tys. zł, **zapisy do 08.10** (czyli dziś) | strona organizatora (nie ustalono) |
| Useme / Oferia (ostatnie 48 h) | niesprawdzone | https://useme.com, https://oferia.pl — przejrzeć ręcznie, filtr „AI / chatbot / automatyzacja” |
| Algora (lista bounty) | niesprawdzone | https://algora.io/bounties |
