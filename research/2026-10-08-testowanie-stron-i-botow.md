# Lokalne testowanie stron i botów LLM (open source)

Odczyt wszystkich źródeł: **2026-10-08**. „(bezp.)” = strona otwarta bezpośrednio; „(wysz.)” = z wyników wyszukiwarki.

## Audyt stron

| Narzędzie | Do czego | Licencja | Offline / lokalnie | Wysiłek | Źródło |
|---|---|---|---|---|---|
| **Lighthouse** | wydajność, dostępność, SEO, dobre praktyki (4 kategorie) | Apache-2.0 | lokalny CLI z Chrome; strona musi być osiągalna z maszyny | niski | [GoogleChrome/lighthouse](https://github.com/GoogleChrome/lighthouse) (bezp.) |
| **Unlighthouse** | Lighthouse dla **całej witryny** naraz, z interfejsem; raporty w `.unlighthouse` | MIT | lokalny CLI (`npx unlighthouse --site …`), Node ≥ 22.18 | niski | [harlan-zw/unlighthouse](https://github.com/harlan-zw/unlighthouse) (bezp.) |
| **Lighthouse CI** | Lighthouse w CI, budżety i asercje, historia wyników na własnym serwerze | Apache-2.0 | serwer LHCI do postawienia samemu; uruchamianie offline **niepotwierdzone** w README | średni | [GoogleChrome/lighthouse-ci](https://github.com/GoogleChrome/lighthouse-ci) (bezp.) |
| **pa11y** (+ pa11y-ci) | dostępność WCAG (A/AA/AAA), silniki axe-core i HTML_CodeSniffer | **LGPL-3.0** | lokalny CLI, Headless Chrome, Node ≥ 22.13 | niski | [pa11y/pa11y](https://github.com/pa11y/pa11y) (bezp.) |
| **linkinator** | zepsute linki, rekurencyjnie (`--recurse`), także pliki lokalne i Markdown | MIT | w pełni lokalny | bardzo niski | [JustinBeckwith/linkinator](https://github.com/JustinBeckwith/linkinator) (bezp.) |

**Niepotwierdzone:** samodzielny crawler SEO open source (np. SEOnaut). Adres sprawdzony w tym badaniu zwrócił 404, więc go nie oceniam.

## Testy botów i LLM

| Narzędzie | Do czego | Licencja | Offline / lokalnie | Wysiłek | Źródło |
|---|---|---|---|---|---|
| **promptfoo** | ewaluacje promptów (asercje w YAML) i red teaming | MIT („pozostaje MIT”) | ewaluacje lokalnie, obsługuje Ollamę. **Telemetria domyślnie włączona**; `PROMPTFOO_DISABLE_TELEMETRY=1`, ale według zgłoszenia #9968 i PR #10047 nadal wychodzi jedno potwierdzenie na uruchomienie. Od 03.2026 część OpenAI. | niski | [repo](https://github.com/promptfoo/promptfoo) (bezp.), [telemetria](https://www.promptfoo.dev/docs/configuration/telemetry/), [#9968](https://github.com/promptfoo/promptfoo/issues/9968) (wysz.) |
| **garak** (NVIDIA) | skaner podatności: prompt injection, jailbreak, wycieki, toksyczność | Apache-2.0 | lokalnie; generator Ollama (`--model_type ollama`), modele HF i GGUF | średni | [NVIDIA/garak](https://github.com/NVIDIA/garak) (bezp.), [docs ollama](https://reference.garak.ai/en/latest/garak.generators.ollama.html) (wysz.) |
| **DeepEval** | metryki jakości (LLM-as-a-judge), testy w stylu pytest | Apache-2.0 | lokalnie z Ollamą jako sędzią (`deepeval set-ollama`); telemetria domyślnie włączona, opt-out `DEEPEVAL_TELEMETRY_OPT_OUT=1`; chmura Confident AI opcjonalna | średni | [repo](https://github.com/confident-ai/deepeval) (bezp.), [docs Ollama](https://deepeval.com/integrations/models/ollama), [prywatność](https://deepeval.com/docs/data-privacy) (wysz.) |

**WNIOSEK:** „offline” wymaga przy promptfoo i DeepEval wyłączenia telemetrii **oraz** blokady wyjścia na poziomie sieci. Przy promptfoo sama zmienna środowiskowa nie wystarcza (#9968).

## Co nadaje się do płatnego audytu SEO dla małych firm

**WNIOSEK:**
- **Rdzeń:** Unlighthouse (cała witryna, czytelny raport), linkinator (zepsute linki), pa11y (WCAG, z axe-core). Wszystkie lokalne, z licencjami pozwalającymi na usługę: MIT, Apache i LGPL przy samym używaniu narzędzia.
- **Dla stałych klientów:** Lighthouse CI z własnym serwerem do miesięcznego śledzenia zmian.
- **Czego brakuje (PRZYPUSZCZENIE):** narzędzia nie sprawdzają treści pod lokalne SEO (profil Google, spójność NAP, opinie). To ręczna część audytu i właśnie za nią klient płaci. Pasuje tu lista 10 kontroli widoczności lokalnej przygotowana wcześniej (poza repozytorium).
- **Uwaga licencyjna:** LGPL-3.0 (pa11y) nie przeszkadza w świadczeniu usługi, ale przy wbudowaniu pa11y w produkt sprzedawany klientowi trzeba spełnić warunki LGPL (**niepotwierdzone** w konkretnym scenariuszu; do sprawdzenia).
- **Testy botów** (garak i promptfoo) mogą być osobną usługą dla firm z czatbotem na stronie: raport z prób wstrzyknięcia poleceń i wycieków danych.
