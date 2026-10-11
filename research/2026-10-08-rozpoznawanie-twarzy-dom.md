# Rozpoznawanie twarzy domowników w Home Assistant (lokalnie)

Odczyt wszystkich źródeł: **2026-10-08**.
„(bezp.)” = strona otwarta bezpośrednio; „(wysz.)” = treść z wyników wyszukiwarki (strona była niedostępna z tego środowiska albo nie była otwierana). `docs.frigate.video` nie rozwiązywało się z DNS, więc dokumentację Frigate czytano z repozytorium (`docs/docs/...`).

## Porównanie

| | **Frigate (wbudowane, od 0.16)** | **Double Take** | **CompreFace** |
|---|---|---|---|
| Co to jest | NVR z detekcją obiektów; twarze jako „enrichment” | Pośrednik: bierze zdarzenia z Frigate, wysyła klatki do zewnętrznego silnika (np. CompreFace) | Samodzielny serwer rozpoznawania twarzy z REST API |
| Licencja kodu | MIT (bez znaków towarowych) — [repo](https://github.com/blakeblackshear/frigate) (bezp.) | MIT — [repo](https://github.com/jakowenko/double-take) (bezp.) | Apache-2.0 — [repo](https://github.com/exadel-inc/CompreFace) (bezp.) |
| Licencja modeli | **Niepotwierdzone** — dokumentacja nie podaje licencji modeli; pobierane raz z GitHuba, potem offline — [face_recognition.md](https://github.com/blakeblackshear/frigate/blob/dev/docs/docs/configuration/face_recognition.md) (bezp.) | zależy od silnika | FaceNet i InsightFace; licencji wag nie podano na stronie (bezp.). Wagi InsightFace (np. buffalo_l): **tylko niekomercyjne badania** — [insightface](https://github.com/deepinsight/insightface), [insightface.ai](https://www.insightface.ai/) (wysz.) |
| AMD | Model `small` (FaceNet) na **CPU** (wymaga AVX+AVX2). Model `large` (ArcFace) „tylko gdy jest zintegrowane/dedykowane GPU/NPU” — (bezp.). Obraz `-rocm`: ROCm wykrywany automatycznie dla enrichmentów, ale „tylko część modeli” — [hardware_acceleration_enrichments.md](https://github.com/blakeblackshear/frigate/blob/dev/docs/docs/configuration/hardware_acceleration_enrichments.md) (bezp.). iGPU AMD „nie jest oficjalnie wspierane przez ROCm”, trzeba ustawić `HSA_OVERRIDE_GFX_VERSION`; gfx1151 **nie jest wymieniony** — [object_detectors.md](https://github.com/blakeblackshear/frigate/blob/dev/docs/docs/configuration/object_detectors.md) (bezp.) | n/d (pośrednik) | „CPU i GPU”, wymaga x86 z AVX (bezp.). AMD/ROCm **niepotwierdzone** |
| Dokładność | Brak liczb; `small` „mniej dokładny” niż `large` (bezp.) | n/d | Brak liczb na stronie (bezp.) |
| Zdjęć na osobę | min. 5–10, dobry start 20–30, idealnie 50–100; trenować partiami po 4–6 podobnych; **brak treningu negatywnego** (bezp.) | brak wskazówek (bezp.) | „wystarczy jedno zdjęcie” — twierdzenie producenta (bezp.) |
| Utrzymanie | 0.16.0 wydane 16.08.2025 — [dyskusja #19536](https://github.com/blakeblackshear/frigate/discussions/19536) (wysz.) | upstream: ostatni tag v1.13.2 (18.08.2025); fork `skrashevich` dalej wydaje 1.13.x — [releases](https://github.com/jakowenko/double-take/releases) (wysz.) | ostatnie wydanie v1.2.0, prawdopodobnie 2023 — [releases](https://github.com/exadel-inc/CompreFace/releases) (wysz.) |

## Jak wywołać powitanie „cześć Tomek” w HA

**FAKT:** Frigate publikuje na MQTT `frigate/tracked_object_update` po każdej próbie rozpoznania (także poniżej progu); pola `name` (najlepsze dopasowanie albo `null`) i `score` (ważona średnia) — [mqtt.md](https://github.com/blakeblackshear/frigate/blob/dev/docs/docs/integrations/mqtt.md) (bezp.). Rozpoznana osoba trafia też jako `sub_label` do zdarzeń i przeglądów (bezp.).
**FAKT:** w HA mowa przez `tts.speak` z encją Piper — [HA: TTS w automatyzacjach](https://www.home-assistant.io/voice_control/using_tts_in_automation/) (wysz.). Użytkownik zgłosił, że podobna automatyzacja przestała działać po aktualizacji Frigate — [forum HA](https://community.home-assistant.io/t/frigate-face-recognition-notification/1018176) (wysz.).

**PRZYPUSZCZENIE (nietestowane):** szkic automatyzacji. Próg 0.9 = domyślny `recognition_threshold` Frigate; `name` może być `null`.

```yaml
alias: Powitanie domownika
mode: single
triggers:
  - trigger: mqtt
    topic: frigate/tracked_object_update
conditions:
  - "{{ trigger.payload_json.type == 'face' }}"
  - "{{ trigger.payload_json.name not in [none, '', 'unknown'] }}"
  - "{{ trigger.payload_json.score | float(0) >= 0.9 }}"
  - "{{ trigger.payload_json.camera == 'wejscie' }}"
actions:
  - action: tts.speak
    target: { entity_id: tts.piper }
    data:
      media_player_entity_id: media_player.salon
      message: "Cześć {{ trigger.payload_json.name }}!"
  - delay: "00:10:00"   # nie witaj co kilka sekund
```

## RODO i AI Act w domu

- **FAKT:** RODO nie stosuje się do przetwarzania „w ramach czynności o czysto osobistym lub domowym charakterze” (art. 2 ust. 2 lit. c). Wyjątek interpretuje się wąsko: kamera obejmująca choćby częściowo przestrzeń publiczną albo posesję sąsiada wypada poza niego — wyrok TSUE C-212/13 Ryneš (11.12.2014) i [Wytyczne EROD 3/2019](https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf) (wysz.). Prezes UODO nakazywał demontaż/przestawienie kamer i nałożył na osobę prywatną karę 26 711 zł — [rp.pl](https://www.rp.pl/dane-osobowe/art43469051-kamery-wycelowane-w-sasiadow-i-droge-prezes-uodo-to-niezgodne-z-prawem), [poradyodo.pl](https://www.poradyodo.pl/aktualnosci/prywatny-monitoring-nie-moze-obejmowac-posesji-sasiadow-ani-drogi-publicznej-13306.html) (wysz.).
- **FAKT:** AI Act nie stosuje się do obowiązków osób fizycznych używających AI „w ramach czysto osobistej, pozazawodowej działalności” (art. 2 ust. 10) — [EUR-Lex 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) (wysz.).
- **WNIOSEK:** kamera z rozpoznawaniem twarzy **wewnątrz domu lub skierowana wyłącznie na własną posesję** mieści się w wyjątku domowym. Kamera na furtkę z widokiem na chodnik — już nie: wtedy dane biometryczne (art. 9 RODO) przechodnia albo listonosza to duży problem.
- **Dzieci — PRZYPUSZCZENIE/zalecenie:** wyjątek domowy obejmuje domowników, ale twarz dziecka to dane biometryczne trwające całe życie. Trzymać bibliotekę twarzy tylko lokalnie, bez kopii w chmurze, z możliwością usunięcia; nie trenować na zdjęciach z innych źródeł.
- **Goście — PRZYPUSZCZENIE/zalecenie:** nie dodawać gości do biblioteki twarzy; Frigate i tak zapisuje próby rozpoznania (`save_attempts`, domyślnie 200 — bezp.), więc ustawić krótką retencję i informować gości (kartka przy wejściu). Opiekunka albo sprzątająca pracująca w domu to już relacja zawodowa — **niepotwierdzone**, czy wyjątek domowy wtedy wystarcza; do konsultacji z prawnikiem.

## Rekomendacja na start

**WNIOSEK:** **Frigate 0.16+ z modelem `small` (CPU)**. Jedno narzędzie zamiast trzech, licencja MIT, aktywnie rozwijane, wynik na MQTT gotowy do HA. Model `large` i obraz `-rocm` dopiero po sprawdzeniu na gfx1151 (brak potwierdzenia wsparcia). Double Take + CompreFace odradzam na start: dwa dodatkowe serwisy, CompreFace bez wydania od ok. 2023, a wagi InsightFace mają licencję niekomercyjną.

**Test akceptacyjny (PRZYPUSZCZENIE):** 20–30 zdjęć na domownika; przez tydzień liczyć w logach MQTT: fałszywe powitania (cel: 0), trafienia przy wejściu (cel: ≥ 80%).
