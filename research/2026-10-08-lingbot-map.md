# LingBot-Map (Robbyant / Ant Group)

Odczyt wszystkich źródeł: **2026-10-08**. „(bezp.)” = strona otwarta bezpośrednio; „(wysz.)” = z wyników wyszukiwarki (arXiv i Hugging Face są niedostępne z tego środowiska).

## Co to jest

- **FAKT:** model „feed-forward” do strumieniowej rekonstrukcji 3D, oparty na architekturze Geometric Context Transformer. Wejście: wideo albo folder zdjęć. Wyjście: chmura punktów, pozycje kamery, predykcje NPZ na klatkę oraz podgląd w przeglądarce. Siatek (mesh) README nie wymienia — [github.com/Robbyant/lingbot-map](https://github.com/Robbyant/lingbot-map) (bezp.).
- **FAKT:** ok. 20 FPS przy 518×378 na sekwencjach powyżej 10 000 klatek — README (bezp.); arXiv v1 z 15.04.2026, v3 z 8.09.2026 — [arXiv 2604.14141](https://arxiv.org/abs/2604.14141) (wysz.). Projekt jest kandydatem do nagrody za najlepszy artykuł ECCV 2026 (README, bezp.).
- **FAKT:** w wersji v1 na Oxford Spires: AUC@15 = 61,64 i ATE = 6,42, wobec VGGT 23,84 / 24,78 (wysz.; w v3 liczby mogą się różnić).
- **FAKT:** autorzy piszą, że rekonstrukcja z jednej kamery „jest z natury niejednoznaczna co do skali”. Skalę ustalają z pierwszych klatek („anchor frames”) — arXiv (wysz.). README nie mówi, że wynik jest w metrach (bezp.).
- **FAKT, ograniczenia z README (bezp.):** trenowany na 320 widokach, przy większej pamięci KV jakość spada; nie resetuje stanu; przy rozjechaniu się pozycji kamery trzeba użyć `--mode windowed`.

## Licencja

- Kod: **Apache-2.0** — README i [profil Robbyant](https://github.com/Robbyant) (bezp.).
- Wagi: **niepotwierdzone**. README nie podaje licencji checkpointów (bezp.). Strona trzecia pisze o Apache-2.0 (wysz.), ale karta modelu na HF nie była czytelna.
- Wagi: `lingbot-map.pt` i `lingbot-map-long.pt` po ok. 4,63 GB, `lingbot-map-stage1.pt` 4,76 GB, `skyseg_batch.onnx` 176 MB — [HF robbyant/lingbot-map](https://huggingface.co/robbyant/lingbot-map/tree/main) (wysz.).

## Wymagania i AMD

- **FAKT:** Python 3.10, PyTorch 2.8.0 z **CUDA 12.8**, opcjonalnie FlashInfer (bez niego `--use_sdpa`), do renderowania NVIDIA Kaolin z rozszerzeniami CUDA. **AMD/ROCm, CPU i MPS nie są wspomniane** — README (bezp.).
- **FAKT:** zgłoszenie [#73](https://github.com/Robbyant/lingbot-map/issues/73) (25.05.2026): karta 4 GB zabrakło pamięci; użytkownik (nie opiekun projektu) podaje ok. 14 GB na T4 i ok. 8 GB po zmianach z #71 (bezp.). Opiekunowie nie podali minimalnych wymagań.
- **FAKT (ogólny):** PyTorch dla ROCm udostępnia AMD przez `torch.cuda` / urządzenie „cuda” (wysz.). Na gfx1151 zgłaszane są jednak błędy dostępu do pamięci w ROCm/PyTorch — [ROCm#5824](https://github.com/ROCm/ROCm/issues/5824), [#5853](https://github.com/ROCm/ROCm/issues/5853) (wysz.).
- **WNIOSEK:** podstawowa rekonstrukcja (`demo.py` z `--use_sdpa`) **może** ruszyć na PyTorch-ROCm, bo nie wymaga FlashInfer. Renderowanie przez Kaolin **nie ruszy** (tylko CUDA). **PRZYPUSZCZENIE:** pamięci 128 GB nie brakuje; ryzykiem jest stabilność ROCm na gfx1151, nie ilość pamięci.

## Do czego realnie w domu i w rolnictwie

**WNIOSEK / PRZYPUSZCZENIE:**
- **Dom, mapa 3D pomieszczeń z telefonu:** realne jako podgląd i dokumentacja, np. „jak wyglądało przed remontem”. **Bez skali w metrach** do pomiarów potrzebny jest przedmiot odniesienia o znanej długości i ręczne przeskalowanie.
- **Rolnictwo, skan budynku lub maszyny z ręki:** dobry kandydat (stała scena, wideo z obchodu). Skala jak wyżej. Do inwentaryzacji „co gdzie stoi” wystarczy, do wymiarów konstrukcyjnych nie.
- **Rolnictwo, pole z ręki:** słabo. Duże, jednorodne powierzchnie (zboże, trawa) i niebo są trudne dla rekonstrukcji z obrazu, a README ma osobne maskowanie nieba. Do pól lepsze są drony z GNSS i fotogrametria (**niepotwierdzone** porównanie).
- **Niepotwierdzone:** brak niezależnej oceny dokładności metrycznej.

**Test na start (PRZYPUSZCZENIE):** 60-sekundowe wideo pokoju z miarką 1 m w kadrze, `demo.py --use_sdpa --mode windowed` na PyTorch-ROCm. Sukces, jeśli przebieg kończy się bez błędu GPU, a długość miarki po przeskalowaniu mieści się w ±5%.
