# Laya — lokalny model decyzyjny

Odczyt wszystkich źródeł: **2026-10-08**. „(bezp.)” = strona otwarta bezpośrednio; „(wysz.)” = z wyników wyszukiwarki. `atomic.chat` nie rozwiązywało się z DNS, a Hugging Face jest zablokowane.

## Co to jest

- **FAKT:** nieautoregresywny model decyzyjny („System 1”). Nie generuje tekstu, tylko odpowiada na typowane pytania: `choice` (jedna z opcji), `noul` (prawdopodobieństwo „tak”) i `score` (skala). Wszystko w jednym przebiegu modelu — [github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) (bezp.).
- **FAKT, autor:** Convai Innovations. Licencja **Apache-2.0** (repo, bezp.).
- **FAKT, checkpointy (bezp.):**

| Checkpoint | Baza | Parametry | Kontekst | Przeznaczenie |
|---|---|---|---|---|
| `laya` | ModernBERT-large | 421M | 512 | angielski |
| `laya-multilingual` | mmBERT-base | 322M | 1024 (do 8192) | „100+ języków” |
| `laya-typed-decisions` | ModernBERT-large | 421M | 1024 | dostrojony do benchmarku typed-decisions |

- **FAKT, uruchamianie lokalne:** `pip install laya`, potem `Router().predict(state, questions)` (bezp.). Format GGUF/Ollama **nie jest wspomniany**; to Python/PyTorch.
- **FAKT, rola Atomic Chat:** promuje Laya jako lokalną alternatywę dla hostowanego Jev 1.13. Wpis „11× szybciej w Tetrisie na MacBooku Air” to wynik z jednego demo, nie benchmark — [X @atomic_chat_hq](https://x.com/atomic_chat_hq/status/2102160983409955244), [atomic.chat blog](https://atomic.chat/blog/guides/jev-1-13-run-locally-laya) (wysz.).

## Jakość (dane autora, niezweryfikowane niezależnie)

- Zero-shot MASSIVE (EN) 0,783; XNLI (EN) 0,860. Wersja wielojęzyczna na tych samych zbiorach po angielsku: 0,657 i 0,843 (bezp.).
- Typed-decisions: 0,766 po dostrojeniu, ale **0,362 dla bazowego checkpointu**, wobec 0,318 przy losowaniu i 0,461 przy wyborze najczęstszej klasy (bezp. + [HF karta](https://huggingface.co/convaiinnovations/laya-typed-decisions), wysz.).
- Autor pisze, że modele są **zbyt pewne siebie** po wydaniu, a `laya-multilingual` nie ma dopasowanej temperatury (bezp.).
- **Język polski: niepotwierdzone.** Repozytorium nie wymienia polskiego. Z 51 testowanych języków 48 jest „użytecznych (>3× losowo)” przy automatycznym wyborze checkpointu, ale bez wyników dla poszczególnych języków (bezp.).
- Słabość przy przeczeniach (zaprzeczona prośba o anulowanie nadal klasyfikowana jako „anuluj”) — [layer3labs](https://www.layer3labs.io/guides/laya-explained) (wysz., źródło wtórne).

## Opóźnienie

| Sprzęt | `laya` | `laya-multilingual` | Źródło |
|---|---|---|---|
| T4, 1 pytanie | 39,5 ms | 32,8 ms | repo (bezp.) |
| CPU (Intel Mac autora, 28 wątków) | 113 ms | 48 ms | repo (bezp.) |
| Pełne wywołanie z wczytaniem na CPU | 193–464 ms | | repo (bezp.) |
| AMD iGPU / ROCm | **niepotwierdzone** | | — |

## Porównanie z API decyzji OpenAI

- **FAKT:** OpenAI Decisions API jest w publicznej becie. Oficjalna dokumentacja mówi o odpowiedziach „ok. 10× szybciej niż Responses API” i **nie podaje liczby w ms** — [developers.openai.com: Decisions](https://developers.openai.com/api/docs/guides/decisions), [ogłoszenie](https://community.openai.com/t/decisions-api-is-now-available-in-public-beta/1403877) (wysz.).
- **„34 ms na link” — niepotwierdzone.** Nie znalazłem tej liczby w źródłach OpenAI. Źródła wtórne podają ok. 150 ms, a jeden nieformalny test mediana 309 ms — [firecrawl](https://www.firecrawl.dev/blog/openai-decisions-api-vs-jev), [techbytes](https://techbytes.app/posts/openai-decisions-api-gpt-6-luna-classification/) (wysz.).
- **WNIOSEK:** Decisions API to usługa w chmurze, więc odpada przy wymogu „bez chmury”. Do porównań uczciwszy jest czas po stronie serwera; dla lokalnej Laya na CPU realnie wychodzi ok. 50–110 ms na pytanie (dane autora).

## Czy nadaje się do „czy to pytanie wymaga internetu”?

- **WNIOSEK:** typ pytania pasuje (`noul`: „Pytanie wymaga aktualnych informacji z internetu”). Licencja i rozmiar też pasują do domowego serwera.
- **Ryzyka:** brak potwierdzonej jakości po polsku, zawyżona pewność i słabość przy przeczeniach („nie szukaj w internecie, tylko…”).
- **PRZYPUSZCZENIE / plan testu:** 100 polskich pytań oznaczonych ręcznie (50 „internet”, 50 „nie”), w tym 10 z przeczeniem. Próg ustalony przed pomiarem: trafność ≥ 90% i opóźnienie p95 ≤ 150 ms na CPU. Porównać z regułą (słowa „dziś”, „teraz”, „pogoda”, „kurs”, „wynik meczu”) oraz z szybkim modelem Ollama odpowiadającym jednym tokenem. Laya ma sens tylko wtedy, gdy wygra z obiema prostszymi metodami.
