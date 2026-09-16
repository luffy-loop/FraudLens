# FraudLens

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask&logoColor=white)
![SHAP](https://img.shields.io/badge/Explainability-SHAP-FF6F61)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?logo=vercel&logoColor=white)
![CI](https://github.com/luffy-loop/FraudLens/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/License-MIT-green)

## Explainable Financial Fraud Detection & Risk Analytics

FraudLens is an end-to-end machine learning application for detecting potentially fraudulent financial transactions. It combines imbalanced classification, probability-based decisions, threshold tuning, a Flask prediction API, batch analysis, model-grounded risk signals, automated testing, monitoring utilities, and SHAP-based local explainability.

## Live Demo

**Try FraudLens:** https://fraud-lens-eight.vercel.app/

**Source Code:** https://github.com/luffy-loop/FraudLens

## Why FraudLens?

Fraud detection is not an accuracy-first classification problem. Fraudulent transactions represent a tiny fraction of the dataset, so FraudLens focuses on precision, recall, F1, ROC-AUC, PR-AUC, and decision-threshold selection rather than accuracy alone.

The project separates validation-based threshold tuning from final test evaluation and keeps model explanations tied to the anonymized features actually available to the model.

## Features

- Individual transaction fraud scoring
- Fraud probability and tuned classification threshold
- Batch prediction for up to 100 transactions
- Input validation and structured API errors
- Model-grounded risk signals
- SHAP-based local explanations
- Interactive transaction inspector
- CSV batch analysis
- Investigation-style prediction reports
- Flask REST API
- Reproducible model packaging with joblib
- Automated API and monitoring tests
- Lightweight prediction monitoring utilities
- GitHub Actions CI

## Architecture

```text
Transaction Data
      ↓
Preprocessing + Scaling
      ↓
Random Forest
      ↓
Fraud Probability
      ↓
Validation-selected Threshold
      ↓
LEGITIMATE / FRAUD
      ↓
┌───────────────┬────────────────┐
│ Risk Signals  │ SHAP Explanation│
└───────────────┴────────────────┘
      ↓
Flask REST API
      ↓
Interactive Frontend
      ↓
Monitoring + Tests
```

## Machine Learning Pipeline

```text
Raw Transaction Data
        ↓
Duplicate Removal
        ↓
Train / Validation / Test Workflow
        ↓
Feature Preprocessing
        ↓
StandardScaler
        ↓
Random Forest Classifier
        ↓
Probability Prediction
        ↓
Validation Threshold Selection
        ↓
Final Test Evaluation
        ↓
Prediction API + Explainability
```

## Model

The current prediction pipeline uses a **Random Forest Classifier**.

| Parameter | Value |
|---|---:|
| Estimators | 100 |
| Maximum Depth | 10 |
| Class Weight | Balanced |
| Random State | 42 |
| Features | 30 |

The trained model is packaged with its preprocessing pipeline so inference applies the same feature transformations used during training.

## Model Performance

The deployed pipeline was evaluated on an untouched test set after threshold selection.

| Metric | Test Result |
|---|---:|
| Precision | **86.59%** |
| Recall | **74.74%** |
| F1 Score | **80.23%** |
| ROC-AUC | **97.46%** |

### Confusion Matrix

| | Predicted Legitimate | Predicted Fraud |
|---|---:|---:|
| Actual Legitimate | 56,640 | 11 |
| Actual Fraud | 24 | 71 |

These results are dataset-specific and should not be interpreted as production financial-system performance.

## Classification Threshold

The decision threshold is selected on validation data using F1 Score and then applied to the untouched test set.

The current packaged model uses:

```text
threshold = 0.60
```

```text
Fraud Probability >= 0.60 → FRAUD
Fraud Probability < 0.60  → LEGITIMATE
```

An older API-testing notebook contains a historical 0.65 output. That notebook result is treated as a historical test artifact rather than the current packaged threshold.

## Explainability

FraudLens uses two complementary explanation layers.

### Model-grounded risk signals

The API combines Random Forest feature importance with standardized feature deviation to surface model-relevant signals.

The source dataset contains anonymized PCA-transformed features `V1–V28`, so the application does not invent business meanings such as merchant type, location, or payment method.

### SHAP local explanations

`src/explainability.py` provides a reusable SHAP-based transaction explainer. It:

1. Loads the packaged model.
2. Applies the same preprocessing pipeline used for inference.
3. Creates a `TreeExplainer` for the Random Forest.
4. Ranks the five features with the largest absolute SHAP contribution.
5. Reports whether each contribution pushes the prediction toward fraud or legitimate classification.

Example output structure:

```json
[
  {
    "feature": "V14",
    "shap_value": 0.18421,
    "direction": "fraud"
  }
]
```

SHAP values describe model contribution, not causal explanations. Because the underlying V-features are anonymized PCA components, they should not be interpreted as human-readable transaction causes.

## Evaluation Plots

`scripts/generate_evaluation_plots.py` provides a reproducible plotting workflow for:

- ROC curve
- Precision-Recall curve
- Confusion matrix

The script expects a dataset containing `Class`, `fraud_probability`, and `prediction` columns. This keeps generated evaluation visuals tied to actual model predictions rather than fabricated values.

Run after creating a prediction-enriched evaluation dataset:

```bash
python scripts/generate_evaluation_plots.py
```

Generated figures are written to:

```text
docs/plots/
```

## REST API

FraudLens exposes the model through Flask endpoints:

```http
GET  /health
POST /predict
POST /predict_batch
```

`/predict` accepts the 30 transaction features:

```text
Time, V1–V28, Amount
```

The response includes fraud probability, threshold, prediction, result, and risk signals.

Batch prediction accepts up to 100 transactions and validates every transaction before inference.

**Full API reference:** `docs/API.md`

## Testing

FraudLens includes automated tests for core API behavior and monitoring utilities.

Run locally with:

```bash
pytest -q
```

The GitHub Actions workflow installs the pinned project dependencies, compiles the Python modules, and runs the test suite on pushes to `main` and pull requests targeting `main`.

## Prediction Monitoring

The `monitoring/` package provides lightweight utilities for observing prediction behavior without changing the deployed inference API.

Current utilities include:

- prediction counts and fraud rate
- mean fraud probability
- validation of probability and threshold inputs
- basic reference-vs-current population shift based on mean probability

These utilities provide a foundation for future drift dashboards and automated alerts.

## Dataset

FraudLens uses the **Credit Card Fraud Detection** dataset containing:

- `Time`
- `V1–V28`
- `Amount`
- `Class`

The raw dataset is not included in the repository because of its size.

Place it locally at:

```text
data/raw/creditcard.csv
```

Original dataset:

```text
Transactions: 284,807
Fraudulent transactions: 492
```

After duplicate removal:

```text
Transactions: 283,726
Fraudulent transactions: 473
```

The extreme class imbalance is a central modelling consideration.

## Handling Class Imbalance

FraudLens uses class weighting during model training:

```python
class_weight="balanced"
```

Evaluation emphasizes:

- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC

## Project Structure

```text
FraudLens/
│
├── api/
│   ├── app.py
│   └── index.py
├── data/
│   └── raw/
│       └── creditcard.csv
├── docs/
│   ├── API.md
│   └── plots/
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── test_transactions.csv
├── models/
│   └── fraud_detection_model.joblib
├── monitoring/
│   ├── __init__.py
│   └── prediction_monitor.py
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_api_testing.ipynb
├── scripts/
│   └── generate_evaluation_plots.py
├── src/
│   └── explainability.py
├── tests/
│   ├── test_api.py
│   └── test_monitoring.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── LICENSE
├── requirements.txt
├── vercel.json
└── README.md
```

## Tech Stack

### Machine Learning

- Python 3.11
- pandas
- NumPy
- scikit-learn
- joblib
- SHAP

### Backend

- Flask
- Flask-CORS
- REST API

### Frontend

- HTML
- CSS
- JavaScript

### Deployment

- Vercel

### Engineering

- GitHub Actions
- pytest
- Git

## Limitations

FraudLens is a portfolio and educational machine learning application, not a production financial fraud detection system.

Important limitations include:

- The dataset contains anonymized PCA features.
- The model does not use merchant, customer, device, or geographic information.
- SHAP and risk signals describe model behavior, not real-world causal fraud reasons.
- Results depend on the underlying dataset and its distribution.
- The classification threshold is tuned for this dataset and may not generalize to another transaction population.
- The current model does not continuously retrain on new financial data.
- No claim is made that the model can replace professional fraud investigation systems.

## Future Improvements

- Integrate SHAP explanations directly into the frontend investigation report
- Persist evaluation plots as versioned model artifacts
- Hyperparameter optimization
- Model drift dashboards
- Automated retraining workflows
- Feature distribution monitoring
- Advanced anomaly detection
- Authentication and API security
- Production-grade deployment infrastructure

These are planned improvements rather than currently implemented capabilities.

## License

This project is licensed under the MIT License.
