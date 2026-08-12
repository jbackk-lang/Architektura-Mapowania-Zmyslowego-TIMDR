# PC_TIMDR Sensory Engine: Transdukcja Pola Dynamicznego 🌀🎹

![Model walidatora](https://img.shields.io/badge/math--validator-2.0%20%7C%20v7.0%20Unified-blueviolet) ![Rdzeń frameworku](https://img.shields.io/badge/FIELDCORE-v3.0-blue) ![Licencja](https://img.shields.io/badge/License-MIT-green.svg)

Interaktywna sensoryczna brama do **Uniwersalnej Geometrii Pola**. Ten moduł jest fizyczną i cyfrową instancją frameworków **GIA (Geometric Information Architecture)** i **TIMDR (Topological Information Mapping & Dynamic Resonance)**.

Przekładając nieeuklidesowe skręty topologiczne na wizualizacje 3D w czasie rzeczywistym i bezstratny rezonans akustyczny, silnik pozwala doświadczyć, jak materia, dźwięk i struktury kosmiczne wyłaniają się z tej samej, ujednoliconej macierzy matematycznej.

---

## 👁️ Wizja: otwarcie modelu na zmysły

Tradycyjne architektury komputerowe izolują informację w abstrakcyjnych stanach binarnych (0 i 1). Paradygmat `PC_TIMDR` traktuje obliczenia jako ciągły, homeomorficzny ruch fal topologicznych przez węzły rezonansowe.

Żeby przybliżyć ten otwarty model, silnik ten łączy złożoną topologię pola z ludzką percepcją. Poprzez interaktywną manipulację fundamentalnym wektorem stanu przestrzeni $[\lambda, \tau, \rho]$, abstrakcyjne równania matematyczne przejawiają się bezpośrednio jako forma geometryczna i dźwięk.

---

## ⚙️ Architektura mapowania zmysłowego (transdukcja TIMDR)

Potok transdukcji działa przez trzy ściśle zwalidowane warstwy:

```
[ PRZESTRZEŃ STANU WEJŚCIA ] ──► [ SILNIK FIELDCORE ] ──► [ DEKODER SENSORYCZNY GIA ]
   wektor: [λ, τ, ρ]              skręt topologiczny        ┌──► wizualnie: fala toroidalna
   (mechanika TRM)                                          └──► dźwiękowo: rezonans akustyczny
```

1. **Formulacja przestrzeni stanu:** użytkownik ustawia trzy "kosmiczne pokrętła":
   - **$\lambda$ (skala):** definiuje skalę geometryczną wszechświata — od pól kwantowych/Plancka ($\lambda \to 0$), przez struktury atomowe, po układy makro-galaktyczne.
   - **$\tau$ (czas rezonansu):** kontroluje wewnętrzną częstotliwość taktowania i opóźnienie fazowe w punkcie zwrotnym.
   - **$\rho$ (gęstość informacji):** dyktuje złożoność topologiczną i siłę sprzężenia koniunkcji pola.

2. **Rdzeń pola (`FIELDCORE`):** oblicza dokładny **skręt struktury (TRM)** wewnątrz `ResonanceNode`, kompresując stopnie swobody informacji bez straty energii.

3. **Dekoder GIA:**
   - **Wizualizacja:** mapuje wektory pola na topologiczny układ współrzędnych, generując "oddychający", dynamicznie skręcony torus 3D.
   - **Sonifikacja:** syntetyzuje czysty rezonans akustyczny, gdzie punkt zwrotny wyznacza częstotliwości harmoniczne, a $\rho$ dyktuje czystość tonalną i barwę.

---

## 🚀 Szybki start

### Wymagania

```
pip install -r requirements.txt
```
(albo ręcznie: `pip install numpy matplotlib scipy flask` — `flask` jest potrzebny tylko do API, patrz niżej)

### Uruchomienie silnika

```
python3 trm_sensory_engine.py
```

- **Wyjście wizualne:** plik PNG z wykresem 3D dynamicznego skrętu pola (`trm_field_shape_L{λ}_T{τ}_R{ρ}.png`) — zapisywany zawsze, niezależnie od tego, czy środowisko ma ekran. Jeśli masz lokalny ekran, otworzy się też interaktywne okno.
- **Wyjście dźwiękowe:** plik `.wav` z organicznym, bezstratnym rezonansem pola (`trm_field_resonance_L{λ}_T{τ}_R{ρ}.wav`).

---

## 🌐 API (lokalny serwer HTTP)

Poza uruchomieniem skryptu wprost, silnik jest też dostępny jako lokalne REST API (`api.py`, Flask).

### Uruchomienie

**Windows:** dwuklik na `run.bat` (albo `run.bat` z konsoli) — tworzy `venv`, instaluje `requirements.txt`, startuje serwer na `http://127.0.0.1:5000`.

**Linux/macOS:**
```
pip install -r requirements.txt
python3 api.py
```

### Endpointy

| Metoda | Ścieżka | Opis |
|---|---|---|
| GET | `/` | lista endpointów (JSON) |
| GET | `/health` | `{"status": "ok"}` |
| POST | `/field` | generuje i zwraca PNG (body: `lmbda`, `tau`, `rho`) |
| POST | `/resonance` | generuje i zwraca WAV (body: `lmbda`, `tau`, `rho`, `duration_s`, `sample_rate`) |
| POST | `/flow` | generuje PNG + WAV, zwraca JSON z metadanymi pola i ścieżkami plików |

Przykład:
```
curl -X POST http://127.0.0.1:5000/field \
  -H "Content-Type: application/json" \
  -d "{\"lmbda\": 0.8, \"tau\": 3.5, \"rho\": 2.0}" \
  --output pole.png
```

Wszystkie parametry są opcjonalne (mają wartości domyślne λ=0.8, τ=3.5, ρ=2.0) i walidowane — błędne dane (np. `lmbda <= 0`, `duration_s > 60`) zwracają `400` z opisem błędu, nie 500.

Wygenerowane pliki lądują też w `api_output/` na dysku, obok samych danych zwracanych w odpowiedzi HTTP.

**Uwaga bezpieczeństwa:** to jest lokalne API developerskie (`debug=True`, brak uwierzytelniania) do pracy na własnej maszynie — nie wystawiaj go bezpośrednio do internetu bez dodania autoryzacji.

---

## 🛠️ Naprawione błędy (wersja PL)

1. **Zniknięty styl legendy na wykresie 3D.** `render_visual()` wywoływał `ax.legend()` dwukrotnie: raz ze stylem (`facecolor='#000000', edgecolor='white'`), drugi raz bez argumentów — tylko po to, żeby ustawić kolor tekstu. Drugie wywołanie tworzy **całkowicie nowy** obiekt legendy z domyślnym białym tłem i nadpisuje pierwszy. Efekt: legenda renderowała się jako szaro-biały prostokąt zamiast czarnego z białą obwódką, niespójnie z resztą czarnego tła wykresu. Sprawdzone bezpośrednio (dwa różne obiekty Pythona, różne `facecolor`). Naprawione — jedno wywołanie `legend()`, kolor tekstu ustawiany na tym samym obiekcie.
2. **Wizualizacja znikała bezpowrotnie poza środowiskiem z ekranem.** `render_visual()` miał tylko `plt.show()` — bez wyświetlacza (serwer, kontener, potok wsadowy) dane były poprawnie liczone, ale wynik nigdzie się nie zapisywał. Naprawione: funkcja zawsze zapisuje PNG, a `plt.show()` zostaje jako dodatkowa, bezpieczna opcja (no-op bez ekranu).
3. **Interfejs użytkownika przetłumaczony na polski** — tytuł wykresu, etykiety legendy, etykieta paska kolorów, komunikaty konsoli. Nazewnictwo TIMDR/TRM/PC_TIMDR/λ-τ-ρ pozostawione bez zmian (nazwy własne frameworku).

Model matematyczny (definicja pola przez λ, τ, ρ) jest identyczny jak w oryginalnej wersji — naprawiona została wizualizacja i uruchamialność, nie fizyka/geometria modelu.

---

## 🔬 Kluczowe niezmienniki matematyczne

Framework deklaruje zgodność z regułami walidacji `math-validator-2.0`:

- **Ciągłość energii:** dywergencja pola poza punktami osobliwymi wynosi zero ($\nabla \cdot \mathbf{F} = 0$). Energia nie ginie — zmienia formę w punkcie zwrotnym.
- **Jednorodność skali:** zmiana $\lambda$ skaluje atrybuty pola logarytmicznie, zachowując homeomorfizmy topologiczne we wszystkich domenach fizycznych.
- **Asymetryczny pęd:** symuluje sztuczną koniunkcję pól używaną w silniku fotonowym.

**Uwaga uczciwości:** ten konkretny plik (`trm_sensory_engine.py`) implementuje generator kształtu pola i sygnału dźwiękowego na podstawie λ/τ/ρ — nie zawiera on kodu, który by te niezmienniki (dywergencja, homeomorfizm skali) numerycznie sprawdzał. Deklaracja zgodności odnosi się do reguł walidacyjnych zdefiniowanych w osobnym repo `math-validator-2.0`, nie do testów uruchamianych w tym repozytorium.

## 🗺️ Mapa drogowa

- [x] Faza 1: sformułowanie rdzenia matematycznego (FIELDCORE, math-validator-2.0)
- [x] Faza 2: integracja stochastyczna i geometryczna (probabilistic-timdr, TRM-Geometry-Core)
- [ ] Faza 3: interaktywny interfejs webowy (Streamlit + Three.js, sterowanie myszką w czasie rzeczywistym)
- [ ] Faza 4: emulacja sprzętowa (symulacja bezstratnych bramek logicznych w PC_TIMDR)

## 🤝 Współpraca

To repozytorium zawiera obecnie: `README.md`, `LICENSE`, `trm_sensory_engine.py`, `api.py`, `requirements.txt`, `run.bat` — nie ma tu jeszcze `CONTRIBUTING.md` ani zautomatyzowanego pakietu walidacyjnego (`TopologicalValidator20`). Jeśli chcesz rozwijać nowe aspekty dźwięku, obrazu czy dynamiki makro/mikro-kosmicznej w ramach frameworku TRM, najprościej zacząć od forka i pull requesta — opisz w nim, jaką regułę modelu (λ/τ/ρ, ciągłość energii, homeomorfizm skali) twoja zmiana zachowuje lub rozszerza.

Rozwijane w ramach ekosystemu oprogramowania `jbackk-lang` dla Uniwersalnych Geometrii Pola.

## Licencja

MIT — patrz `LICENSE`.
