"""
flow_script.py — przykladowe uzycie TIMDER Multisensory Meditation Engine.

Uruchomienie z katalogu glownego repo:
    python3 examples/flow_script.py

(skrypt sam dodaje katalog glowny repo do sys.path, wiec dziala z
dowolnego katalogu roboczego)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.rhythm_engine import RhythmEngine
from core.color_engine import ColorEngine
from core.light_engine import LightEngine
from core.image_engine import generate_fractal
from core.signal_engine import generate_pulse
from core.integrator import Integrator


def main():
    rhythm = RhythmEngine().generate(bpm=60, pattern="skręt")
    color = ColorEngine().palette(mode="Λ-relax")
    light = LightEngine().sequence(pattern="τ-soft")
    image = generate_fractal(preset="ρ-smooth", size=128, render=False)
    signal = generate_pulse(level=1.0, mode="pulse", duration_s=5.0, sample_rate=100.0)

    flow = Integrator().flow(rhythm, color, light, image, signal)
    print(flow)


if __name__ == "__main__":
    main()
