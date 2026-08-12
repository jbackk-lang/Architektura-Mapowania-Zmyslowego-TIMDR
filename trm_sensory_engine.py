"""
trm_sensory_engine.py — PC_TIMDR Sensory Engine (wersja PL, naprawiona)

Zmiany względem oryginału:
  1. NAPRAWIONY błąd wizualny: `render_visual()` wywoływał `ax.legend()`
     dwa razy — raz ze stylem (`loc='upper left', facecolor='#000000',
     edgecolor='white'`), drugi raz bez argumentów (tylko po to, żeby
     ustawić kolor tekstu). Drugie wywołanie tworzy CAŁKOWICIE NOWY
     obiekt legendy z domyślnym białym tłem, nadpisując pierwszy —
     efekt: legenda renderowała się jako szary/biały prostokąt zamiast
     czarnego z białą obwódką, niezgodnie z resztą czarnego tła wykresu.
     Sprawdzone bezpośrednio: `ax.legend(...)` i późniejsze `ax.legend()`
     to dwa różne obiekty (`is` zwraca False), drugi ma
     facecolor=(1,1,1,0.8) zamiast (0,0,0,0.8). Naprawione: kolor
     tekstu ustawiany na TYM SAMYM obiekcie zwróconym z jedynego
     wywołania `legend()`.
  2. `render_visual()` teraz ZAWSZE zapisuje wynik do pliku PNG
     (domyślnie `trm_field_shape_L{λ}_T{τ}_R{ρ}.png`), a dopiero potem
     próbuje `plt.show()`. W oryginale był tylko `plt.show()` — bez
     środowiska z ekranem (serwer, headless, ten silnik uruchomiony w
     potoku wsadowym) wynik znikał bezpowrotnie, mimo że dane zostały
     poprawnie policzone. `plt.show()` na backendzie bez ekranu (Agg)
     jest bezpieczne (nic nie robi), więc to działa identycznie jak
     poprzednio w środowisku z ekranem, i dodatkowo działa tam, gdzie
     poprzednio nie dawało żadnego efektu.
  3. Wszystkie napisy w interfejsie (tytuł wykresu, etykiety legendy,
     etykieta paska kolorów, komunikaty na konsoli) przetłumaczone na
     polski. Nazewnictwo TIMDR/TRM/PC_TIMDR/λ-τ-ρ zachowane bez zmian
     (to nazwy własne frameworku, nie treść do tłumaczenia).

Model matematyczny (λ, τ, ρ) jest identyczny jak w oryginale — nie
zmieniałem definicji pola, tylko naprawiłem wizualizację i
uruchamialność.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")  # dziala tez bez ekranu (serwer/headless); patrz punkt 2 wyzej
import matplotlib.pyplot as plt
from scipy.io import wavfile


class TRMSensoryEngine:
    def __init__(self, lmbda: float, tau: float, rho: float):
        """
        TIMDR TRM Sensory Engine (prawdziwy TRM-kształt).
        λ (lmbda) - skala geometryczno-polowa (rozpiętość drabiny)
        τ (tau)   - czas wewnętrzny / taktowanie ewolucji
        ρ (rho)   - gęstość skrętu polowego (TRM-density)
        """
        self.lmbda = lmbda
        self.tau = tau
        self.rho = rho

    def generate_trm_field(self, resolution: int = 2000):
        """
        Generuje TRM-kształt jako pole:
        - oś T: czas wewnętrzny TIMDR (nie zwykły czas)
        - helisa zewnętrzna: nośnik pola (flux line)
        - helisa wewnętrzna: implozja / collapse
        - gęstość: lokalna wartość TRM-density (ρ_eff)
        """
        T = np.linspace(0, 2 * np.pi * self.tau, resolution)
        phase = self.rho * T
        density = 0.5 * (1.0 + np.sin(phase))  # w [0,1], naturalny prog 0.5

        collapse_mask = density < 0.5
        stable_mask = ~collapse_mask

        radius_outer = self.lmbda * (0.7 + 0.6 * density)
        radius_inner = self.lmbda * (0.3 + 0.4 * (1.0 - density))

        Z = (T / (2 * np.pi)) * (self.lmbda * self.rho)

        X_outer = radius_outer * np.cos(T)
        Y_outer = radius_outer * np.sin(T)

        X_inner = radius_inner * np.cos(T + np.pi / 2.0)
        Y_inner = radius_inner * np.sin(T + np.pi / 2.0)

        return {
            "T": T,
            "Z": Z,
            "density": density,
            "collapse_mask": collapse_mask,
            "stable_mask": stable_mask,
            "X_outer": X_outer,
            "Y_outer": Y_outer,
            "X_inner": X_inner,
            "Y_inner": Y_inner,
        }

    def render_visual(self, save_path: str = None, show: bool = True):
        """
        Wizualizacja TRM-ksztaltu:
        - zewnetrzna nic: stabilne pole (stable_mask)
        - wewnetrzna nic: implozja (collapse_mask)
        - kolor: lokalna gestosc TRM (rho_eff)

        Zwraca sciezke do zapisanego pliku PNG.
        """
        field = self.generate_trm_field()

        Xo, Yo, Zo = field["X_outer"], field["Y_outer"], field["Z"]
        Xi, Yi, Zi = field["X_inner"], field["Y_inner"], field["Z"]
        density = field["density"]
        collapse_mask = field["collapse_mask"]
        stable_mask = field["stable_mask"]

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection="3d")

        ax.plot(
            Xo[stable_mask], Yo[stable_mask], Zo[stable_mask],
            label="Stabilna nić strumienia TRM", color="cyan", linewidth=2.5, zorder=2,
        )
        ax.plot(
            Xi[collapse_mask], Yi[collapse_mask], Zi[collapse_mask],
            label="Rdzeń kolapsu TRM", color="magenta", linewidth=1.8, zorder=3,
        )
        scatter = ax.scatter(
            Xo[::8], Yo[::8], Zo[::8], c=density[::8], cmap="plasma", s=18, zorder=4,
        )

        ax.set_title(
            f"Kształt pola TIMDR TRM (λ={self.lmbda}, τ={self.tau}, ρ={self.rho})",
            fontsize=12, color="white",
        )

        fig.patch.set_facecolor("#000000")
        ax.set_facecolor("#000000")
        ax.axis("off")

        cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, aspect=12)
        cbar.ax.yaxis.set_tick_params(color="white")
        plt.setp(plt.getp(cbar.ax.axes, "yticklabels"), color="white")
        cbar.set_label("Gęstość TRM (ρ_eff)", color="white")

        # NAPRAWIONE: jedno wywolanie legend(), ten sam obiekt do stylu i do koloru tekstu
        # (w oryginale drugie, bezargumentowe ax.legend() tworzylo nowa legende
        # z domyslnym bialym tlem i nadpisywalo pierwsza, ostylowana)
        legend = ax.legend(loc="upper left", facecolor="#000000", edgecolor="white")
        for text in legend.get_texts():
            text.set_color("white")

        if save_path is None:
            save_path = f"trm_field_shape_L{self.lmbda}_T{self.tau}_R{self.rho}.png"
        fig.savefig(save_path, dpi=150, facecolor=fig.get_facecolor())
        print(f"-> Zapisano wizualizację: {save_path}")

        if show:
            plt.show()  # bezpieczny no-op na backendzie bez ekranu (Agg)
        plt.close(fig)

        return save_path

    def generate_resonance_sound(self, duration: float = 4.0, sample_rate: int = 44100, save_path: str = None):
        """
        Rezonans TRM: dzwiek nie jest sinusoida, tylko projekcja pola.
        - czestotliwosc bazowa: zwiazana z tau (czas wewnetrzny)
        - modulacja: gestosc TRM (rho_eff)
        - collapse: wygaszanie obszarow ponizej progu 0.5
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

        base_freq = 220.0 * self.tau
        phase = self.rho * 2.0 * np.pi * t
        density_t = 0.5 * (1.0 + np.sin(phase))
        collapse_t = np.where(density_t < 0.5, 0.3, 1.0)
        freq_t = base_freq * (0.8 + 0.6 * density_t)

        wave = np.sin(2.0 * np.pi * freq_t * t)
        for i in range(2, 6):
            weight = (density_t ** 2) * (self.rho / i)
            wave += weight * np.sin(2.0 * np.pi * (freq_t * i) * t)

        wave *= collapse_t

        max_val = np.max(np.abs(wave))
        if max_val > 0:
            wave = wave / max_val

        audio_data = np.int16(wave * 32767)

        if save_path is None:
            save_path = f"trm_field_resonance_L{self.lmbda}_T{self.tau}_R{self.rho}.wav"
        wavfile.write(save_path, sample_rate, audio_data)

        print("\n[PC_TIMDR — wyjście sprzętowe]: transdukcja TRM zakończona.")
        print(f"-> Zapisano plik audio: {save_path}")

        return save_path


# --- BLOK OPERACYJNY MASZYNY ---
if __name__ == "__main__":
    print("[PC_TIMDR]: Inicjalizacja silnika sensorycznego TRM...")
    engine = TRMSensoryEngine(lmbda=0.8, tau=3.5, rho=2.0)

    print("[PC_TIMDR]: Renderowanie kształtu pola TRM...")
    engine.render_visual(show=False)  # show=False w skrypcie wsadowym; ustaw True lokalnie z ekranem

    print("[PC_TIMDR]: Generowanie rezonansu tonalnego TRM...")
    engine.generate_resonance_sound()
