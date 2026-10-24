from pathlib import Path
from math import radians, sin, cos, isfinite
import joblib
import pandas as pd
from flask import Flask, request, jsonify

HERE = Path(__file__).resolve().parent
bundle = joblib.load(HERE / "models/model_bundle.joblib")
model = bundle["pipeline"]
app = Flask(__name__)


def prepare_input(values):
    """Validate five form values and convert aspect into sine/cosine."""
    required = bundle["raw_features"]
    if not isinstance(values, dict) or set(values) != set(required):
        raise ValueError("Please provide exactly these fields: " + ", ".join(required))

    for field in required:
        if isinstance(values[field], bool) or not isinstance(values[field], (int, float)):
            raise ValueError(field + " must be a number")
        if not isfinite(values[field]):
            raise ValueError(field + " must be finite")

    if not 0 <= values["slope_deg"] <= 90:
        raise ValueError("Slope must be between 0 and 90")
    if not 0 <= values["aspect_deg"] < 360:
        raise ValueError("Aspect must be between 0 and less than 360")
    if values["precip_total_mm"] < 0:
        raise ValueError("Rainfall cannot be negative")

    angle = radians(values["aspect_deg"])
    row = {
        "elevation_m": values["elevation_m"],
        "slope_deg": values["slope_deg"],
        "aspect_sin": sin(angle),
        "aspect_cos": cos(angle),
        "temp_mean_c": values["temp_mean_c"],
        "precip_total_mm": values["precip_total_mm"],
    }
    return pd.DataFrame([row], columns=bundle["features"])


@app.get("/health")
def health():
    return jsonify(status="ok", features=bundle["raw_features"], model_version=bundle["model_version"])


@app.post("/predict")
def predict():
    try:
        data = request.get_json(silent=True)
        features = prepare_input(data)
        class_number = int(model.predict(features)[0])  # 0, 1 or 2
        forest_id = bundle["class_codes"][class_number]  # 1, 10 or 20
        probabilities = model.predict_proba(features)[0].tolist()
        return jsonify(
            prediction=forest_id,
            label=bundle["class_labels"][forest_id],
            probabilities={str(bundle["class_codes"][i]): p for i, p in enumerate(probabilities)},
            model_version=bundle["model_version"],
            disclaimer="Teaching demonstration using map-derived labels; not validated for forestry decisions.",
        )
    except (ValueError, TypeError) as error:
        return jsonify(error=str(error)), 400
    except Exception:
        app.logger.exception("Model prediction failed")
        return jsonify(error="Prediction failed"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
