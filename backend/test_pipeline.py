"""Test that a saved model can predict without starting Flask."""
import json
import math
from pathlib import Path
import joblib
import pandas as pd

here = Path(__file__).resolve().parent
bundle = joblib.load(here / "models/model_bundle.joblib")
values = json.loads((here / "test_payload.json").read_text(encoding="utf-8"))
angle = math.radians(values["aspect_deg"])
row = {
    "elevation_m": values["elevation_m"],
    "slope_deg": values["slope_deg"],
    "aspect_sin": math.sin(angle),
    "aspect_cos": math.cos(angle),
    "temp_mean_c": values["temp_mean_c"],
    "precip_total_mm": values["precip_total_mm"],
}
features = pd.DataFrame([row], columns=bundle["features"])
internal_class = int(bundle["pipeline"].predict(features)[0])
forest_class = bundle["class_codes"][internal_class]
print("Prediction:", bundle["class_labels"][forest_class])
print("PASS: direct model inference")
