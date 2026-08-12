📘 MODEL.md — TIMDER Multisensory Meditation Engine (TMME)
Model do modelowania multisensorycznej medytacji geometrycznej TIMDER

🔹 1. Cel modelu
Model TMME definiuje strukturę i zasady działania multisensorycznej medytacji geometrycznej opartej na protokole TIMDER.
Jego zadaniem jest dostarczenie spójnego, neutralnego technologicznie modelu, który można wykorzystać w:

systemach audio (DAW),

instalacjach LED,

VR/AR,

aplikacjach terapeutycznych,

projektach naukowych,

systemach eksperymentalnych.

Model nie generuje fizycznych bodźców — opisuje logikę, strukturę, parametry i przepływ.

🔹 2. Architektura modelu
Model składa się z pięciu silników sensorycznych oraz jednego integratora:

Silniki sensoryczne
RhythmEngine — generuje rytm skrętu (muzyka)

ColorEngine — generuje psycho‑geometrię Λ (kolor)

LightEngine — generuje modulację τ (światło)

ImageEngine (core/image_engine.py) — generuje defekt ρ (obraz); jedyny silnik z realnym renderingiem (fraktale Mandelbrota/Julii, zapis do PNG bez zewnętrznych bibliotek)

SignalEngine (core/signal_engine.py) — generuje klucz J (sygnał); realna próbkowanie w czasie (tryby stable/pulse/wave/burst/sweep)

Uwaga: ImageEngine i SignalEngine nie są klasami — to moduły z funkcjami
`generate_fractal()` i `generate_pulse()`. RhythmEngine, ColorEngine,
LightEngine i Integrator SĄ klasami. Ta niespójność jest celowa (image/
signal engine przeszły przez redesign v2, patrz nagłówki tych plików) —
przykład w sekcji 6 poniżej używa poprawnego API dla obu wariantów.

Integrator
Integrator — łączy pięć kanałów w jeden strumień TIMDER‑FLOW

🔹 3. Modele TIMDER
Model wykorzystuje trzy podstawowe struktury TIMDER:

Model skrętu
Opisuje intensywność i gładkość skrętu — podstawowej jednostki informacji.

Model LTR
Warstwy Λ–τ–ρ jako stan struktury, transformacji i defektu.

Model klucza J
Poziom i tryb klucza J — stabilizatora przepływu.

Model FLOW
Metadane strumienia TIMDER‑FLOW.

🔹 4. Przepływ TIMDER‑FLOW
Strumień multisensoryczny jest tworzony według schematu:

Kod
RhythmEngine → ColorEngine → LightEngine → ImageEngine → SignalEngine → Integrator
Każdy silnik generuje własny model, a integrator łączy je w jeden spójny strumień.

🔹 5. Zasady działania modelu
Neutralność technologiczna  
Model nie zakłada konkretnej platformy — może być użyty w dowolnym środowisku.

Modularność  
Każdy silnik działa niezależnie i może być wymieniony lub rozszerzony.

Deterministyczność  
Te same parametry → ten sam model → przewidywalne wyniki.

TIMDER‑zgodność  
Model jest zgodny z zasadami TIMDER: skręt, Λ–τ–ρ, J‑klucz, rytm, defekt.

🔹 6. Przykład przepływu (poprawiony, zgodny z rzeczywistym API — patrz examples/flow_script.py)
Kod
from core.rhythm_engine import RhythmEngine
from core.color_engine import ColorEngine
from core.light_engine import LightEngine
from core.image_engine import generate_fractal
from core.signal_engine import generate_pulse
from core.integrator import Integrator

rhythm = RhythmEngine().generate(bpm=60, pattern="skręt")
color  = ColorEngine().palette(mode="Λ-relax")
light  = LightEngine().sequence(pattern="τ-soft")
image  = generate_fractal(preset="ρ-smooth", size=128, render=False)
signal = generate_pulse(level=1.0, mode="pulse", duration_s=5.0)

flow = Integrator().flow(rhythm, color, light, image, signal)

Poprzednia wersja tej sekcji (`ImageEngine.fractal(...)`, `SignalEngine.pulse(...)`)
odwoływała się do API sprzed redesignu v2 tych dwóch modułów i nie
działała z aktualnym kodem — poprawione tutaj i w examples/flow_script.py.

🔹 7. Zastosowania modelu
Model może być wykorzystany do:

tworzenia muzyki geometrycznej,

projektowania terapii sensorycznych,

sterowania światłem LED,

generowania wizualizacji VR/AR,

badań nad multisensoryczną modulacją,

eksperymentów z synchronizacją bodźców.
