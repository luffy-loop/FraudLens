from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import math


MAX_BATCH_SIZE = 100


REQUIRED_FEATURES = [
    "Time",
    "V1", "V2", "V3", "V4", "V5", "V6", "V7",
    "V8", "V9", "V10", "V11", "V12", "V13", "V14",
    "V15", "V16", "V17", "V18", "V19", "V20", "V21",
    "V22", "V23", "V24", "V25", "V26", "V27", "V28",
    "Amount"
]


app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

CORS(app)


# Load trained FraudLens model
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model_package = joblib.load(
    BASE_DIR / "models" / "fraud_detection_model.joblib"
)

model = model_package["model"]
threshold = model_package["threshold"]

FEATURE_SIGNAL_COUNT = 3

FEATURE_LABELS = {
    "V14": "V14",
    "V10": "V10",
    "V12": "V12",
    "V17": "V17",
    "V4": "V4",
    "V3": "V3",
    "V11": "V11",
    "V16": "V16",
    "V2": "V2",
    "V9": "V9",
}


def get_risk_signals(features):
    preprocessor = model.named_steps["preprocessor"]
    classifier = model.named_steps["model"]

    transformed = preprocessor.transform(features)

    feature_names = preprocessor.get_feature_names_out()
    importances = classifier.feature_importances_

    ranked_features = sorted(
        zip(feature_names, importances, transformed[0]),
        key=lambda item: item[1],
        reverse=True
    )

    signals = []

    for feature_name, importance, value in ranked_features:
        clean_name = feature_name.replace("num__", "")

        if clean_name not in FEATURE_LABELS:
            continue

        deviation = abs(float(value))

        if deviation >= 2:
            level = "High deviation"
        elif deviation >= 1:
            level = "Moderate deviation"
        else:
            level = "Low deviation"

        signals.append({
            "feature": FEATURE_LABELS[clean_name],
            "importance": round(float(importance), 4),
            "deviation": round(deviation, 2),
            "level": level
        })

        if len(signals) == FEATURE_SIGNAL_COUNT:
            break

    return signals

@app.route("/", methods=["GET"])
def home():
    return send_from_directory("../frontend", "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data provided"
        }), 400

    missing_features = [
        feature
        for feature in REQUIRED_FEATURES
        if feature not in data
    ]

    if missing_features:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing_features
        }), 400

    try:
        values = [data[feature] for feature in REQUIRED_FEATURES]

        if not all(
            isinstance(value, (int, float)) and math.isfinite(value)
            for value in values
        ):
            return jsonify({
                "error": "All feature values must be finite numbers"
            }), 400

        features = pd.DataFrame(
            [values],
            columns=REQUIRED_FEATURES
        )

        probability = model.predict_proba(features)[0][1]

        prediction = int(probability >= threshold)

        result = "FRAUD" if prediction == 1 else "LEGITIMATE"

        risk_signals = get_risk_signals(features)

        return jsonify({
            "prediction": prediction,
            "result": result,
            "fraud_probability": round(float(probability), 6),
            "threshold": threshold,
            "risk_signals": risk_signals
        })

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed"
        }), 500


@app.route("/predict_batch", methods=["POST"])
def predict_batch():
    data = request.get_json()

    if not data or "transactions" not in data:
        return jsonify({
            "error": "No transactions provided"
        }), 400

    transactions = data["transactions"]

    if not isinstance(transactions, list) or len(transactions) == 0:
        return jsonify({
            "error": "Transactions must be a non-empty list"
        }), 400

    if len(transactions) > MAX_BATCH_SIZE:
        return jsonify({
            "error": f"Maximum batch size is {MAX_BATCH_SIZE} transactions"
        }), 400

    results = []

    try:
        for index, transaction in enumerate(transactions):

            missing_features = [
                feature
                for feature in REQUIRED_FEATURES
                if feature not in transaction
            ]

            if missing_features:
                return jsonify({
                    "error": f"Missing features in transaction {index + 1}",
                    "missing_features": missing_features
                }), 400

            values = [
                transaction[feature]
                for feature in REQUIRED_FEATURES
            ]

            if not all(
                isinstance(value, (int, float)) and math.isfinite(value)
                for value in values
            ):
                return jsonify({
                    "error": (
                        "All feature values must be finite numbers "
                        f"in transaction {index + 1}"
                    )
                }), 400

            features = pd.DataFrame(
                [values],
                columns=REQUIRED_FEATURES
            )

            probability = model.predict_proba(features)[0][1]

            prediction = int(probability >= threshold)

            result = "FRAUD" if prediction == 1 else "LEGITIMATE"

            results.append({
                "transaction": index + 1,
                "fraud_probability": round(float(probability), 6),
                "prediction": prediction,
                "result": result
            })

        return jsonify({
            "total_transactions": len(results),
            "results": results
        })

    except Exception:
        app.logger.exception("Batch prediction failed")
        return jsonify({
            "error": "Batch prediction failed"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)