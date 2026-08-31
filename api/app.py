from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)
CORS(app)
# Load trained FraudLens model
model_package = joblib.load(
    "models/fraud_detection_model.joblib"
)

model = model_package["model"]
threshold = model_package["threshold"]


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

    required_features = [
        "Time",
        "V1", "V2", "V3", "V4", "V5", "V6", "V7",
        "V8", "V9", "V10", "V11", "V12", "V13", "V14",
        "V15", "V16", "V17", "V18", "V19", "V20", "V21",
        "V22", "V23", "V24", "V25", "V26", "V27", "V28",
        "Amount"
    ]

    missing_features = [
        feature for feature in required_features
        if feature not in data
    ]

    if missing_features:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing_features
        }), 400

    try:
        features = pd.DataFrame(
            [[data[feature] for feature in required_features]],
            columns=required_features
        )

        probability = model.predict_proba(features)[0][1]

        prediction = int(probability >= threshold)

        result = "FRAUD" if prediction == 1 else "LEGITIMATE"

        return jsonify({
            "prediction": prediction,
            "result": result,
            "fraud_probability": round(float(probability), 6),
            "threshold": threshold
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

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

    required_features = [
        "Time",
        "V1", "V2", "V3", "V4", "V5", "V6", "V7",
        "V8", "V9", "V10", "V11", "V12", "V13", "V14",
        "V15", "V16", "V17", "V18", "V19", "V20", "V21",
        "V22", "V23", "V24", "V25", "V26", "V27", "V28",
        "Amount"
    ]

    results = []

    try:

        for index, transaction in enumerate(transactions):

            missing_features = [
                feature
                for feature in required_features
                if feature not in transaction
            ]

            if missing_features:
                return jsonify({
                    "error": f"Missing features in transaction {index + 1}",
                    "missing_features": missing_features
                }), 400

            features = pd.DataFrame(
                [[transaction[feature] for feature in required_features]],
                columns=required_features
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

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(debug=True)
