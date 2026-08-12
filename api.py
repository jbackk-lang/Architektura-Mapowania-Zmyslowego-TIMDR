"""
api.py — lokalne REST API dla PC_TIMDR Sensory Engine.

Uruchomienie:
    python3 api.py
    (albo run.bat na Windows -- patrz plik run.bat)

Domyślnie nasłuchuje na http://127.0.0.1:5000

Endpointy:
    GET  /                 -- informacje o API (lista endpointów, JSON)
    GET  /health            -- {"status": "ok"}
    POST /field              -- generuje wizualizację PNG dla podanych λ,τ,ρ
                                 body JSON: {"lmbda": 0.8, "tau": 3.5, "rho": 2.0}
                                 zwraca plik PNG (Content-Type: image/png)
    POST /resonance           -- generuje rezonans WAV dla podanych λ,τ,ρ
                                 body JSON: {"lmbda":.., "tau":.., "rho":..,
                                             "duration_s": 4.0, "sample_rate": 44100}
                                 zwraca plik WAV (Content-Type: audio/wav)
    POST /flow                -- generuje PNG + WAV na raz, zwraca JSON z
                                 metadanymi pola (gęstość, maski) i ścieżkami
                                 do wygenerowanych plików (nie samymi plikami --
                                 użyj /field i /resonance, żeby je pobrać)

Wszystkie POST-y przyjmują JSON, walidują parametry (400 przy błędnych
danych) i zapisują wygenerowane pliki do katalogu api_output/.

To jest lokalne API developerskie (debug=True, brak uwierzytelniania) --
NIE wystawiaj tego bezpośrednio do internetu bez dodania autoryzacji.
"""
import io
import os

from flask import Flask, jsonify, request, send_file

from trm_sensory_engine import TRMSensoryEngine

app = Flask(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _parse_lmbda_tau_rho(payload: dict):
    try:
        lmbda = float(payload.get("lmbda", 0.8))
        tau = float(payload.get("tau", 3.5))
        rho = float(payload.get("rho", 2.0))
    except (TypeError, ValueError):
        return None, ("lmbda/tau/rho muszą być liczbami", 400)

    if lmbda <= 0 or tau <= 0 or rho <= 0:
        return None, ("lmbda/tau/rho muszą być > 0", 400)

    return (lmbda, tau, rho), None


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "name": "PC_TIMDR Sensory Engine API",
        "endpoints": {
            "GET /health": "sprawdzenie stanu serwera",
            "POST /field": "generuje wizualizację PNG (body: lmbda, tau, rho)",
            "POST /resonance": "generuje rezonans WAV (body: lmbda, tau, rho, duration_s, sample_rate)",
            "POST /flow": "generuje PNG + WAV, zwraca metadane i ścieżki plików",
        },
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/field", methods=["POST"])
def field():
    payload = request.get_json(silent=True) or {}
    params, error = _parse_lmbda_tau_rho(payload)
    if error:
        return jsonify({"error": error[0]}), error[1]
    lmbda, tau, rho = params

    engine = TRMSensoryEngine(lmbda=lmbda, tau=tau, rho=rho)
    save_path = os.path.join(OUTPUT_DIR, f"trm_field_shape_L{lmbda}_T{tau}_R{rho}.png")
    engine.render_visual(save_path=save_path, show=False)

    return send_file(save_path, mimetype="image/png")


@app.route("/resonance", methods=["POST"])
def resonance():
    payload = request.get_json(silent=True) or {}
    params, error = _parse_lmbda_tau_rho(payload)
    if error:
        return jsonify({"error": error[0]}), error[1]
    lmbda, tau, rho = params

    try:
        duration_s = float(payload.get("duration_s", 4.0))
        sample_rate = int(payload.get("sample_rate", 44100))
    except (TypeError, ValueError):
        return jsonify({"error": "duration_s/sample_rate muszą być liczbami"}), 400

    if duration_s <= 0 or duration_s > 60:
        return jsonify({"error": "duration_s musi być w zakresie (0, 60] sekund"}), 400
    if sample_rate <= 0:
        return jsonify({"error": "sample_rate musi być > 0"}), 400

    engine = TRMSensoryEngine(lmbda=lmbda, tau=tau, rho=rho)
    save_path = os.path.join(OUTPUT_DIR, f"trm_field_resonance_L{lmbda}_T{tau}_R{rho}.wav")
    engine.generate_resonance_sound(duration=duration_s, sample_rate=sample_rate, save_path=save_path)

    return send_file(save_path, mimetype="audio/wav")


@app.route("/flow", methods=["POST"])
def flow():
    payload = request.get_json(silent=True) or {}
    params, error = _parse_lmbda_tau_rho(payload)
    if error:
        return jsonify({"error": error[0]}), error[1]
    lmbda, tau, rho = params

    engine = TRMSensoryEngine(lmbda=lmbda, tau=tau, rho=rho)

    png_path = os.path.join(OUTPUT_DIR, f"trm_field_shape_L{lmbda}_T{tau}_R{rho}.png")
    wav_path = os.path.join(OUTPUT_DIR, f"trm_field_resonance_L{lmbda}_T{tau}_R{rho}.wav")

    engine.render_visual(save_path=png_path, show=False)
    engine.generate_resonance_sound(save_path=wav_path)

    field = engine.generate_trm_field()
    density = field["density"]

    return jsonify({
        "lmbda": lmbda,
        "tau": tau,
        "rho": rho,
        "density_mean": float(density.mean()),
        "density_min": float(density.min()),
        "density_max": float(density.max()),
        "collapse_fraction": float(field["collapse_mask"].mean()),
        "png_path": png_path,
        "wav_path": wav_path,
    })


if __name__ == "__main__":
    print("[PC_TIMDR API]: startuję na http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
