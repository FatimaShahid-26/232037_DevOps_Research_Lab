"""STEP 1: Train four forest classifiers and save the best one."""
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

PROJECT = Path(__file__).resolve().parents[1]
INPUTS = ["elevation_m", "slope_deg", "aspect_sin", "aspect_cos", "temp_mean_c", "precip_total_mm"]
FORM_INPUTS = ["elevation_m", "slope_deg", "aspect_deg", "temp_mean_c", "precip_total_mm"]
FOREST_NAMES = {1: "Naturally regenerating forest", 10: "Primary forest", 20: "Planted/plantation forest"}

# Load the two CSV files produced in Phase 4.
train = pd.read_csv(PROJECT / "data/forest_train_spatial.csv")
test = pd.read_csv(PROJECT / "data/forest_test_spatial.csv")
assert set(train.tile_id).isdisjoint(set(test.tile_id)), "Train/test tiles overlap!"
assert train[INPUTS].notna().all().all() and test[INPUTS].notna().all().all()

# Use the original forest IDs for every algorithm, including XGBoost.
# XGBoost requires 0,1,2, so we convert labels for ALL models.
encode = {1: 0, 10: 1, 20: 2}
decode = {0: 1, 1: 10, 2: 20}
X = train[INPUTS]
y = train.forest_type.map(encode)
X_small, X_validation, y_small, y_validation = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# KNN needs scaled values. Other models use raw values.
models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=12, min_samples_leaf=5, class_weight="balanced", random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=250, min_samples_leaf=2, class_weight="balanced_subsample", random_state=42, n_jobs=-1),
    "KNN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=9, weights="distance")),
    "XGBoost": XGBClassifier(n_estimators=250, max_depth=5, learning_rate=0.05, subsample=0.85,
                            colsample_bytree=0.9, objective="multi:softprob", eval_metric="mlogloss", random_state=42),
}

# Compare four models on development data only.
results = []
for name, model in models.items():
    model.fit(X_small, y_small)
    prediction = model.predict(X_validation)
    accuracy = accuracy_score(y_validation, prediction)
    macro_f1 = f1_score(y_validation, prediction, average="macro")
    results.append({"model": name, "validation_accuracy": round(accuracy, 5), "validation_macro_f1": round(macro_f1, 5)})
    print(f"{name}: accuracy={accuracy:.3f}, macro-F1={macro_f1:.3f}")

# Pick the highest macro-F1 model. Retrain on the whole training CSV.
best = max(results, key=lambda row: (row["validation_macro_f1"], row["validation_accuracy"]))
model = models[best["model"]]
model.fit(X, y)
print("Selected model:", best["model"])

# ONLY NOW inspect the geographically separate test tile.
test_predictions = model.predict(test[INPUTS])
true_labels = test.forest_type.map(encode)
report = {
    "selected_model": best["model"],
    "development_comparison": results,
    "spatial_test_accuracy": accuracy_score(true_labels, test_predictions),
    "spatial_test_macro_f1": f1_score(true_labels, test_predictions, average="macro"),
    "per_class_report": classification_report(true_labels, test_predictions, labels=[0,1,2],
                                                target_names=list(FOREST_NAMES.values()), output_dict=True, zero_division=0),
    "confusion_matrix": confusion_matrix(true_labels, test_predictions, labels=[0,1,2]).tolist(),
    "warning": "Forest labels are map-derived; random development validation may be optimistic."
}

# Save model AND names together so the Flask application can reload them.
bundle = {
    "pipeline": model,
    "features": INPUTS,
    "raw_features": FORM_INPUTS,
    "class_labels": FOREST_NAMES,
    "class_codes": decode,
    "task": "classification",
    "model_version": "lab-baseline-1.0",
}
(PROJECT / "backend/models").mkdir(exist_ok=True)
(PROJECT / "docs").mkdir(exist_ok=True)
joblib.dump(bundle, PROJECT / "backend/models/model_bundle.joblib")
(PROJECT / "docs/model_evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("Spatial test accuracy:", round(report["spatial_test_accuracy"], 3))
print("Spatial test macro-F1:", round(report["spatial_test_macro_f1"], 3))
print("DONE: model_bundle.joblib and model_evaluation.json saved")
