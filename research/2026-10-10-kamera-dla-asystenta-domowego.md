# Kamera dla lokalnego asystenta domowego — research zakupowo-techniczny

**Data odczytu wszystkich źródeł: 2026-10-10.**

## Zasady i ograniczenia

**Oznaczenia źródeł:**
- **(bezp.)** — strona przeczytana bezpośrednio.
- **(wysz.)** — tylko wynik wyszukiwarki lub artykuł z drugiej ręki. Do potwierdzenia przed zakupem.
- **„niepotwierdzone”** — nie znalazłem źródła.

**Oznaczenia treści:** **F** = FAKT, **W** = WNIOSEK, **P** = PRZYPUSZCZENIE.

**Ograniczenie środowiska:** proxy blokuje docs.frigate.video, support.reolink.com, ceneo.pl i x-kom.pl. Dlatego:
- dokumentację Frigate czytałem z repozytorium na GitHubie (gałąź `master`; może wyprzedzać wydanie stabilne);
- **wszystkie ceny pochodzą z wyników wyszukiwarki (wysz.)** i trzeba je sprawdzić w sklepie przed zakupem.

## Wnioski w skrócie

1. **Frigate (oprogramowanie do analizy obrazu z kamer) na Strix Halo:** najlepsza ścieżka to NPU (XDNA2) przez społecznościowy sidecar `frigate-xdna`. Dokumentacja Frigate wprost pisze, że ta ścieżka jest „qualified on Ryzen AI Max 300 / Strix Halo”. GPU przez ROCm działa tylko z ręcznym ustawieniem zmiennej `HSA_OVERRIDE_GFX_VERSION`, bo gfx1151 nie jest na liście automatycznego mapowania (F, bezp.).
2. **Upadek i dym nie powinny zależeć od kamery.** Wykrywanie upadku z obrazu w prawdziwych domach daje dużo fałszywych alarmów (F, wysz.). Do dymu służy certyfikowana czujka dymu, a do obecności w pokoju dziecka — radar zamiast kamery (W).
3. **Kamera tylko do salonu i kuchni**, przewodowa (PoE) i w odciętej sieci VLAN bez internetu (W).
   - Tapo i EZVIZ wymagają aplikacji producenta przy pierwszym uruchomieniu (F, wysz.).
   - Dokumentacja Frigate odradza kamery Wi-Fi (F, bezp.).

## 1. Ranking kamer

### Źródła wspólne dla tabeli

- **Dokumentacja Frigate, sprzęt** (bezp.): https://raw.githubusercontent.com/blakeblackshear/frigate/master/docs/docs/frigate/hardware.md
  - „I recommend Dahua, Hikvision, and Amcrest in that order”.
  - „WiFi cameras are not recommended”.
  - Reolink: „best to stick with 5MP and lower”.
- **Zakaz FCC (USA), 26.06.2026** (wysz.): FCC zabroniła dalszego importu i sprzedaży także sprzętu Hikvision i Dahua certyfikowanego przed 2022 r.; nowe certyfikacje są zablokowane od 11.2022. https://www.sdmmag.com/articles/101401-fcc-expands-ban-on-hikvision-dahua-and-other-chinese-firms
- **UE:** ogólnounijnego zakazu **nie znalazłem**; IPVM pisze o braku polityki UE (raport bez daty) (wysz.): https://ipvm.com/reports/hikua-bans

### Tabela

| # | Model | Cena PL (wysz.) | RTSP/ONVIF bez chmury | Obraz / noc | Mikrofon: wyłączenie sprzętowe | Przesłona / prywatność | Zasilanie | Znane problemy | Producent / ryzyko |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Hikvision DS-2CD2143G2-LI 2.8 mm** (kopułka) | 499 zł, [Neonet](https://www.neonet.pl/p/1334878-kamera-ip-hikvision-ds-2cd2143g2-li-28mm-4-mp.html) | Frigate poleca markę; wiele strumieni o konfigurowalnych parametrach (F, bezp.). Konfiguracja przez przeglądarkę bez aplikacji: **P** | 4 MP; podczerwień: niepotwierdzone dla wariantu -LI | niepotwierdzone (wariant z mikrofonem to zwykle „-IS”: **P**) | brak przesłony (niepotwierdzone) | **PoE** | sufiksy wariantów różnią się wyposażeniem — sprawdzić kartę katalogową | Chiny; zakaz FCC w USA (wysz.) |
| 2 | **Dahua IPC-HDW1439V-A-IL** | 420,35 zł, [cdr.pl](https://cdr.pl/k305,monitoring,,164,dahua-technology.html) — **oferta niedostępna** | Frigate stawia markę na 1. miejscu (F, bezp.) | 4 MP | jest mikrofon (oferta, wysz.); wyłączenie sprzętowe niepotwierdzone | niepotwierdzone | **PoE** | sklep opisuje model jako zewnętrzny | Chiny; zakaz FCC (wysz.) |
| 3 | **Reolink E1 Pro** | 244,99 zł, [Kaufland](https://www.kaufland.pl/product/443785692/); [x-kom V2](https://www.x-kom.pl/p/1129321-inteligentna-kamera-reolink-e1-pro-v2-bialy.html) | Oficjalne FAQ Reolink: obie wersje sprzętowe obsługują ONVIF i RTSP (F, wysz.). Usługi trzeba włączyć w aplikacji lub kliencie Reolink (wysz.) | niepotwierdzone (V1 i V2 się różnią) | niepotwierdzone | niepotwierdzone | Wi-Fi | zgłoszenia, że RTSP przestał działać po aktualizacji firmware (wysz., community.reolink.com) | Chiny (Shenzhen) — **P** |
| 4 | **Reolink E1 Zoom (V2)** | 356,91–429 zł, [Piri](https://www.piri.shop/pl/p/Kamera-obrotowa-Reolink-E1-Zoom-8Mpx-4K-Dwuzakresowe-Wifi-Zdalny-podglad/130), [Eltrox](https://www.eltrox.pl/p/40419-kamera-ip-wifi-reolink-e1-zoom-v2) | RTSP/ONVIF bezpośrednio (niezależny przewodnik „verified July 2026”, wysz.) | 5 MP (V2, [Allegro](https://allegro.pl/produkt/kamera-reolink-e1-zoom-v2-wewnetrzna-5mp-smart-4c83e88f-a270-4cf1-92fc-f8aff7383718)) **lub** 8 MP 4K ([Kaufland](https://www.kaufland.pl/product/433930099/)) — **wybrać 5 MP** | niepotwierdzone | „Privacy mode” blokuje widok i zatrzymuje dźwięk. Ustawiany tylko w aplikacji ≥ 4.49, nie w kliencie (wysz., [Reolink](https://support.reolink.com/articles/37046076925209-Introduction-to-Reolink-Privacy-Mode/)) | Wi-Fi | Frigate: Reolink 4K+ sprawia problemy (F, bezp.) | jak wyżej |
| 5 | **TP-Link Tapo C225** | 178,99 zł, [x-kom](https://www.x-kom.pl/p/1107005-inteligentna-kamera-tp-link-tapo-c225-obrotowa-kamera-wi-fi.html) | RTSP po założeniu „Camera Account” **w aplikacji Tapo** (wysz.). Użytkownik forum HA pisze, że potrzebne jest konto w chmurze (wysz., niepotwierdzone oficjalnie) | 2K — niepotwierdzone | brak przełącznika sprzętowego w źródłach; tryb prywatności z aplikacji wstrzymuje obraz i dźwięk (wysz.) | **Fizyczna:** „lens is blocked by the housing” ([karta katalogowa](https://static.tp-link.com/upload/product-overview/2023/202302/20230215/Tapo%20C225(EU)1.0_Datasheet.pdf), wysz.) | Wi-Fi | **wymaga aplikacji przy pierwszym uruchomieniu** | Chiny / USA — **P** |
| 6 | **EZVIZ C6N** | nie sprawdzono | RTSP z kodem z naklejki; **lokalny serwer RTSP trzeba włączyć w aplikacji EZVIZ** ([dokumentacja HA](https://www.home-assistant.io/integrations/ezviz/), wysz.) | niepotwierdzone | niepotwierdzone | niepotwierdzone | Wi-Fi / LAN | jedna recenzja przeczy obsłudze RTSP (wysz.) | marka Hikvision — **P** |
| 7 | **Ubiquiti G6 Instant** | nie znalazłem ceny PL | Wymaga konsoli UniFi Protect (lokalnej). Bezpośredni RTSP z kamery: **niepotwierdzone** (wysz.) | 4K/30 kl./s, noc (wysz.) | niepotwierdzone | niepotwierdzone | Wi-Fi albo PoE z adapterem (wysz.) | dodatkowy koszt konsoli | USA — **P** |
| 8 | **Axis M1075-L** | nie znalazłem ceny PL | niepotwierdzone (dziś nie sprawdzałem) | 1080p, czujnik ruchu PIR, praca w 0–35 °C ([karta PL](https://www.axis.com/dam/public/8d/08/b8/datasheet-axis-m1075-l-box-camera-pl-PL-520273.pdf), wysz.) | dwukierunkowe audio (wysz.); wyłączenie sprzętowe niepotwierdzone | niepotwierdzone | PoE — **P** | — | Szwecja — **P** |
| — | **ESP32-CAM (ESPHome)** | — | strumień przez ESPHome; z Frigate bywa niestabilny ([forum HA](https://community.home-assistant.io/t/esp32-cam-and-frigate/603766), wysz.) | niska rozdzielczość, przegrzewanie przy wysokim kl./s (wysz.) | zależy od płytki | — | Wi-Fi | **nie nadaje się do rozpoznawania twarzy** (W) | — |

**Nie znalazłem w polskich sklepach:** Amcrest i Imou. Dla Imou nie znalazłem źródła o RTSP bez aplikacji.

### Które wymagają aplikacji lub chmury mimo RTSP

- **F (wysz.):**
  - Tapo — konto kamery zakłada się w aplikacji.
  - EZVIZ — RTSP włącza się w aplikacji.
  - Reolink — tryb prywatności tylko w aplikacji; RTSP/ONVIF włącza się w aplikacji lub w programie Reolink Client.
  - Ubiquiti — potrzebna konsola UniFi (lokalna).
- **W:** wszystko po pierwszej konfiguracji da się zamknąć w VLAN bez internetu. **P:** Hikvision i Dahua konfiguruje się przez przeglądarkę, bez aplikacji i konta — do sprawdzenia na konkretnym egzemplarzu.

**Mikrofon:** w żadnym modelu nie znalazłem potwierdzonego **sprzętowego** wyłącznika mikrofonu.
- **W:** wybrać wariant bez mikrofonu albo wyłączyć audio w kamerze i nie pobierać ścieżki audio w go2rtc i Frigate.

## 2. Oprogramowanie lokalne

| Element | FAKT | Źródło |
|---|---|---|
| Frigate — wersja | v0.18.0, 12.09 (oznaczona „Latest”; obraz `0.18.0-rocm`). Rok nie jest podany na stronie | [releases](https://github.com/blakeblackshear/frigate/releases) (bezp.) |
| AMD przez ROCm | Od 0.16 osobny detektor ROCm usunięto; należy użyć `type: onnx` | jw. (bezp.) |
| AMD — zintegrowane GPU | „AMD/ROCm does not "officially" support integrated GPUs”. Automatyczne mapowanie obejmuje tylko gfx1031 i gfx1103, **gfx1151 nie ma**, więc potrzebny jest `HSA_OVERRIDE_GFX_VERSION`. Problemy przy konwersji modeli do formatu mxr | [object_detectors.md](https://raw.githubusercontent.com/blakeblackshear/frigate/master/docs/docs/configuration/object_detectors.md) (bezp.) |
| **AMD NPU (XDNA2)** | „AMD Ryzen AI / XDNA2 NPUs can run object detection through the community-maintained `frigate-xdna` ZMQ sidecar … qualified on Ryzen AI Max 300 / Strix Halo” | jw. (bezp.) |
| Szybkość na Strix Halo (NPU) | YOLOv9 przy wejściu 320 px: tiny ~7,4 ms, small ~9,0 ms, C ~14,1 ms. Dokumentacja poleca YOLOv9-C 320 | [hardware.md](https://raw.githubusercontent.com/blakeblackshear/frigate/master/docs/docs/frigate/hardware.md) (bezp.) |
| Szybkość na GPU AMD 780M (ROCm) | YOLOv9 tiny 320: ~14 ms | jw. (bezp.) |
| Zawieszanie detekcji na iGPU AMD (780M) | Maintainer: to raczej problem firmware lub sterownika | [dyskusja #19853](https://github.com/blakeblackshear/frigate/discussions/19853) (wysz.) |
| OpenVINO / CPU | OpenVINO działa na CPU AMD „despite having no official support”. Detektor CPU „not recommended for general use” | object_detectors.md (bezp.) |
| Wbudowane rozpoznawanie twarzy | Model small (FaceNet, CPU) i large (ArcFace, wymaga GPU/NPU). Zalecane 20–30 zdjęć na osobę. Obraz z podczerwieni (czarno-biały) jest słabym materiałem. Wynik trafia do `sub_label`. **„requires a one-time internet connection to download … models from GitHub”**. Nie łączyć z Double Take | [face_recognition.md](https://raw.githubusercontent.com/blakeblackshear/frigate/master/docs/docs/configuration/face_recognition.md) (bezp.) |
| GenAI (opis obrazu) | Ollama obsługiwana natywnie. Polecany `qwen3-vl` (obsługuje też wywołania narzędzi dla HA). Zalecane `OLLAMA_NUM_PARALLEL=1` | [genai/config.md](https://raw.githubusercontent.com/blakeblackshear/frigate/master/docs/docs/configuration/genai/config.md) (bezp.) |
| Integracja z HA | Instalacja przez HACS, **wymaga MQTT**, licencja MIT. Encje: liczniki obiektów, ruch, migawki | [frigate-hass-integration](https://github.com/blakeblackshear/frigate-hass-integration) (bezp.) |
| Double Take | Fork `skrashevich/double-take`, MIT. Daty ostatniego commita nie widać | [repo](https://github.com/skrashevich/double-take) (bezp.) |
| CompreFace | Apache-2.0, CPU i GPU, wymaga AVX. Daty ostatniego wydania nie widać | [repo](https://github.com/exadel-inc/CompreFace) (bezp.) |

**Wnioski:**
- **W:** rozpoznawanie twarzy wbudowane we Frigate wystarcza. Double Take i CompreFace to dodatkowe usługi bez zysku.
- **W:** modele twarzy trzeba pobrać **przed** odcięciem serwera od internetu albo podać je ręcznie. Blokada dotyczy kamer; serwer może mieć kontrolowany dostęp.

**Liczba kamer i opóźnienia:**
- **P:** ~9 ms na detekcję na NPU to około 100 detekcji/s. Przy detekcji 5 kl./s daje to kilka do kilkunastu kamer. **Pomiaru dla gfx1151 i NPU w praktyce nie znalazłem.**
- **Opóźnienie od zdarzenia do automatyzacji w HA:** niepotwierdzone (brak źródła). Zmierzyć samemu: znacznik czasu zdarzenia w MQTT a moment wykonania automatyzacji.

## 3. Upadek, osoba leżąca, dym

| Zadanie | Dojrzałość | Źródło |
|---|---|---|
| Upadek z obrazu w prawdziwym domu | **Demo / badania.** 11/11 upadków wykrytych, ale **5,4 fałszywego alarmu dziennie** (próba 7-dniowa, 2011). Studium wdrożenia: „very high recall … lacks precision … false positives (more than 99 per-cent)”. Główne przyczyny: światło z okien i kilka osób w pokoju | [RESNA 2011](https://www.resna.org/sites/default/files/legacy/conference/proceedings/2011/RESNA_ICTA/belshaw-69411.pdf), [HAL 03904734](https://hal.uca.fr/hal-03904734) (wysz.) |
| Upadek z radaru: Aqara FP2 | Producent: montaż sufitowy wymagany do wykrywania upadków; „not a medical device”. Działa lokalnie przez HomeKit Controller, ale **pierwsza konfiguracja wymaga aplikacji i chmury Aqara**, zmiana stref też | [Aqara](https://aqara.cn/us/product/presence-sensor-fp2/), [privatehomelab](https://privatehomelab.com/aqara-fp2-home-assistant-local/) (wysz.) |
| Obecność z radaru: LD2410 (ESPHome) | Dojrzałe do obecności (`has_target`, 9 stref odległości). **Nie wykrywa upadku** | [ESPHome LD2410](https://esphome.io/components/sensor/ld2410.html) (wysz.) |
| Dym | Detekcji dymu z obrazu we Frigate **nie znalazłem**. Frigate ma detektory dźwięku (plik `audio_detectors.md` istnieje, bezp.); czy rozpoznają sygnał czujki dymu — niepotwierdzone | — |

**Wnioski:**
- **W:** do dymu certyfikowana czujka dymu z integracją HA. Kamera nie jest systemem przeciwpożarowym.
- **W:** upadek = radar (FP2 to kompromis z jednorazowym kontaktem z chmurą) plus potwierdzenie głosowe przez Voice PE („Czy wszystko w porządku?”). Kamera tylko jako drugie potwierdzenie (osoba nieruchoma w strefie podłogi).

## 4. Prywatność i prawo w PL

| Kwestia | FAKT / WNIOSEK | Źródło |
|---|---|---|
| Wyłączenie domowe | **F:** RODO art. 2 ust. 2 lit. c nie obejmuje przetwarzania „w ramach czynności o czysto osobistym lub domowym charakterze”. TSUE w sprawie Ryneš (C-212/13) zawęża to wyłączenie: kamera obejmująca przestrzeń publiczną nie jest już czysto domowa | [eulawradar](https://eulawradar.com/case-c-21213-rynes-data-from-private-cctv-cameras-overlooking-public-spaces-and-private-homes/), [Grant Thornton](https://grantthornton.pl/publikacja/monitoring-prywatny-a-rodo-czy-mozna-miec-kamery-na-swojej-posesji/) (wysz.) |
| Praktyka UODO | **F:** kara 26 711 zł dla właściciela domu, którego kamery obejmowały posesję sąsiada i drogę | [gazetaprawna](https://www.gazetaprawna.pl/prawnik/orzecznictwo/artykuly/10967676,koniec-z-monitoringiem-wokol-domu-decyzja-prezesa-uodo-nie-pozostawia.html) (wysz.) |
| Goście | **W:** kamera wewnątrz domu zostaje w wyłączeniu domowym, ale goście powinni wiedzieć o kamerze (kartka lub komunikat asystenta). **Obowiązku prawnego oznakowania w domu nie znalazłem** | — |
| Opiekunka lub niania (praca zarobkowa w domu) | **P:** wyłączenie domowe może nie objąć nagrywania osoby zatrudnionej; trzeba ją wprost poinformować. Źródła dotyczącego niani **nie znalazłem** — skonsultować z prawnikiem | — |
| Kamera w pokoju dziecka | **F:** stanowiska RPD o kamerach w domu **nie znalazłem**. RPD w 10.2025 krytykował monitoring w placówkach (ryzyko utraty zaufania i poczucia bycia obserwowanym) | [wystąpienie RPD](https://brpd.gov.pl/wp-content/uploads/2025/10/wystapienie-genralne-do-Ministry-Rodziny-Pracy-i-Polityki-Spolecznej-w-sprawie-monitoringu-wizyjnego.pdf) (wysz.) |
| Dźwięk | **F:** poradniki wskazują, by nie nagrywać dźwięku, bo bywa traktowane jak podsłuch | wynik wyszukiwania do muratordom/rp.pl (wysz.) |
| Przechowywanie | **W:** domyślnie bez nagrań ciągłych; tylko migawki zdarzeń z retencją 24–72 h; nagrania nie opuszczają serwera | — |

## 5. Rekomendacja

**Na start (salon lub kuchnia): Hikvision DS-2CD2143G2-LI 2.8 mm, 499 zł, [Neonet](https://www.neonet.pl/p/1334878-kamera-ip-hikvision-ds-2cd2143g2-li-28mm-4-mp.html) (wysz.).**
- **Za:** PoE (stabilnie), marka polecana przez Frigate.
- **Ryzyko producenta (zakaz FCC)** neutralizuje odcięta sieć VLAN bez internetu (W).
- Przed zakupem potwierdzić w karcie katalogowej podczerwień i brak mikrofonu.

**Tańsza alternatywa: Reolink E1 Pro, ok. 245 zł ([Kaufland](https://www.kaufland.pl/product/443785692/), wysz.).**
- RTSP/ONVIF potwierdzone w FAQ producenta.
- Wi-Fi (gorzej według Frigate).
- Wymaga aplikacji lub klienta Reolink przy włączaniu RTSP.

**Odradzam przy tych wymaganiach:** Tapo (aplikacja, prawdopodobnie konto), EZVIZ (aplikacja), ESP32-CAM (jakość).

**Pokój dziecka:** **radar zamiast kamery (W).** LD2410 z ESPHome (w 100% lokalny, tylko obecność) albo Aqara FP2, jeśli potrzebny upadek (jednorazowy kontakt z chmurą). Ceny FP2: 269 zł [Komputronik](https://www.komputronik.pl/product/826327/aqara-presence-sensor-fp2-ps-s02d.html) / 299 zł [x-kom](https://www.x-kom.pl/p/1138112-czujnik-aqara-czujnik-obecnosci-fp2.html) (wysz.). Ceny LD2410 nie sprawdzałem.

### Plan wdrożenia w 5 krokach

1. **Zakup:** kamera PoE + przełącznik lub wstrzykiwacz PoE. Przed zakupem sprawdzić cenę i sufiks modelu w sklepie.
2. **Sieć:**
   - osobny VLAN „kamery”, a na routerze reguła **deny** dla ruchu z tego VLAN-u do internetu;
   - dozwolony tylko ruch serwer → kamera (RTSP 554 / ONVIF);
   - stałe IP; NTP z serwera lokalnego.
   - Test: kamera nie pinguje 1.1.1.1.
3. **go2rtc:** jeden strumień z kamery, pobierany raz; z go2rtc korzystają Frigate i HA. Ścieżka audio wyłączona.
4. **Frigate 0.18 (`-rocm`) + sidecar `frigate-xdna`:**
   - YOLOv9-C 320 na NPU;
   - rozpoznawanie twarzy (model large, 20–30 zdjęć na domownika w świetle dziennym);
   - strefa „podłoga”;
   - GenAI wyłączony na start.
5. **Automatyzacja HA (przez MQTT):**
   - `sub_label` = domownik → asystent wie, z kim rozmawia; brak rozpoznania → tryb „gość” (bez danych prywatnych);
   - osoba nieruchoma w strefie podłogi ponad 60 s **i** radar pokazuje obecność → pytanie głosowe, brak odpowiedzi → powiadomienie;
   - dym obsługuje wyłącznie czujka.
   - Zmierzyć opóźnienie od zdarzenia do akcji.
