from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap

FEATURES = [
    "Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9",
    "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18",
    "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27",
    "V28", "Amount"
]


def load_model(path=None):
    root = Path(__file__).resolve().parent.parent
    path = Path(path) if path else root / "models" / "fraud_detection_model.joblib"
    package = joblib.load(path)
    return package["model"], package["threshold"]


@lru_cache(maxsize=1)
def _get_explainer(model):
    return shap.TreeExplainer(model.named_steps["model"])


def explain_transaction(transaction, model=None):
    if model is None:
        model, _ = load_model()

    row = pd.DataFrame([transaction], columns=FEATURES)
    pre = model.named_steps["preprocessor"]
    transformed = pre.transform(row)
    names = [n.replace("num__", "") for n in pre.get_feature_names_out()]

    values = _get_explainer(model).shap_values(transformed)
    if isinstance(values, list):
        values = values[1]
    values = np.asarray(values)
    if values.ndim == 3:
        values = values[:, :, 1]

    row_values = values[0]
    ranked = sorted(
        zip(names, row_values), key=lambda x: abs(float(x[1])), reverse=True
    )

    return [
        {
            "feature": name,
            "shap_value": round(float(value), 6),
            "direction": "fraud" if value > 0 else "legitimate"
        }
        for name, value in ranked[:5]
    ]
