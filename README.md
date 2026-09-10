# FraudLens

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-REST%20API-000000?logo=flask&logoColor=white)
![Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?logo=vercel&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Explainable Financial Fraud Detection & Risk Analytics

> An end-to-end fraud detection system combining imbalanced classification,
> threshold optimization, REST API inference, batch analysis, and
> model-grounded risk signals.
## Explainable Financial Fraud Detection & Risk Analytics

FraudLens is an end-to-end machine learning application for detecting potentially fraudulent financial transactions through a trained Random Forest classifier, a prediction API, and an interactive web interface.

The project focuses on the practical challenges of financial fraud detection, including severe class imbalance, probability-based classification, threshold tuning, batch prediction, and model-grounded risk signals.

---

## 🚀 Live Demo

**Try FraudLens:**  
https://fraud-lens-eight.vercel.app/

**Source Code:**  
https://github.com/luffy-loop/FraudLens

---

## 🎯 What FraudLens Does

FraudLens provides a complete transaction-analysis workflow:

- Detect potentially fraudulent transactions
- Return fraud probability for individual transactions
- Apply a tuned classification threshold
- Analyze transactions through a web interface
- Process multiple transactions through batch prediction
- Validate transaction inputs before prediction
- Display model-driven risk signals
- Present model performance metrics
- Expose the trained model through a Flask API

---

## 🧠 Machine Learning Pipeline

FraudLens follows this workflow:

```text
Raw Transaction Data
        ↓
Duplicate Removal
        ↓
Train / Test Split
        ↓
Feature Preprocessing
        ↓
StandardScaler
        ↓
Random Forest Classifier
        ↓
Probability Prediction
        ↓
Threshold = 0.60
        ↓
LEGITIMATE / FRAUD
        ↓
Risk Signals + API Response
        ↓
Frontend Investigation Report
```

The model is implemented as a scikit-learn pipeline combining preprocessing and classification.

---

## 🤖 Model

The current production model is a:

**Random Forest Classifier**

Configuration:

| Parameter | Value |
|---|---:|
| Estimators | 100 |
| Maximum Depth | 10 |
| Class Weight | Balanced |
| Random State | 42 |
| Features | 30 |

The model uses a `StandardScaler` through a `ColumnTransformer` before classification.

---

## 📊 Model Performance

The model was evaluated on an untouched test set after threshold selection.

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

These metrics demonstrate that the model can identify a large proportion of fraudulent transactions while maintaining relatively high precision.

---

## 🎚️ Classification Threshold

FraudLens does not simply use the default 0.50 probability threshold.

A validation split was used to evaluate thresholds from **0.10 to 0.90**, with F1 Score used as the selection criterion.

The best validation threshold was:

```text
0.60
```

The selected threshold was then applied to the untouched test set.

Therefore:

```text
Fraud Probability >= 0.60
        ↓
      FRAUD

Fraud Probability < 0.60
        ↓
   LEGITIMATE
```

This separates **threshold selection** from **final model evaluation**, avoiding the use of test labels to tune the decision boundary.

---

## 🔍 Explainability & Risk Signals

FraudLens provides model-grounded risk signals alongside each individual prediction.

The dataset contains anonymized PCA-transformed features:

```text
V1 – V28
```

Because these features are anonymized principal components, they do not have directly interpretable business meanings such as:

- Merchant category
- Geographic location
- Customer occupation
- Payment method

FraudLens therefore avoids inventing semantic explanations for these features.

Instead, the application combines:

- Random Forest feature importance
- Transaction-level standardized feature deviation
- The strongest model-relevant features

to produce signals such as:

```text
V14
High deviation

Model importance: 20.40%
Deviation: 3.14σ
```

This approach communicates what the model is responding to without claiming that an anonymized PCA component represents a specific real-world transaction attribute.

### Most Important Model Features

The current Random Forest identifies the following features among its strongest contributors:

| Feature | Importance |
|---|---:|
| V14 | 20.40% |
| V10 | 11.55% |
| V12 | 10.31% |
| V17 | 9.58% |
| V4 | 9.36% |
| V3 | 6.90% |
| V11 | 5.72% |
| V16 | 4.35% |
| V2 | 3.91% |
| V9 | 2.55% |

Feature importance indicates how strongly the trained model uses a feature across its decision trees; it does not imply that the feature has a human-readable causal meaning.

---

## 🌐 Prediction API

FraudLens exposes the trained model through a Flask REST API.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Single Prediction

```http
POST /predict
```

The endpoint expects the following 30 features:

```text
Time
V1 – V28
Amount
```

Example response:

```json
{
  "prediction": 0,
  "result": "LEGITIMATE",
  "fraud_probability": 0.526994,
  "threshold": 0.6,
  "risk_signals": [
    {
      "feature": "V14",
      "importance": 0.204,
      "deviation": 3.14,
      "level": "High deviation"
    }
  ]
}
```

### Batch Prediction

```http
POST /predict_batch
```

The API supports batch transaction analysis with validation and a maximum batch size of **100 transactions**.

---

## 🖥️ Frontend

The FraudLens interface is designed as a financial-security investigation dashboard rather than a simple model demo.

It provides:

### Quick Analysis

Analyze a predefined sample transaction through the prediction API.

### Batch Analysis

Upload a transaction CSV containing:

```text
Time, V1–V28, Amount
```

Transactions are validated before being sent to the batch prediction endpoint.

### Transaction Inspector

Manually enter transaction features and inspect the resulting model prediction.

### Investigation Report

Each individual prediction presents:

- Fraud probability
- Classification threshold
- Final decision
- Model-driven risk signals
- Recommended action

---

## 📁 Project Structure

```text
FraudLens/
│
├── api/
│   └── app.py
│
├── data/
│   └── raw/
│       └── creditcard.csv
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── test_transactions.csv
│
├── models/
│   └── fraud_detection_model.joblib
│
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_api_testing.ipynb
│
├── monitoring/
│
├── src/
│
├── tests/
│
├── .gitignore
└── README.md
```

---

## 📦 Dataset

FraudLens uses the **Credit Card Fraud Detection** dataset.

The dataset contains:

- `Time`
- `V1–V28`
- `Amount`
- `Class`

The raw dataset is not included in the repository because of its size.

Place it locally at:

```text
data/raw/creditcard.csv
```

### Dataset Characteristics

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

Fraud represents only a very small fraction of the dataset, making class imbalance an important part of the modelling problem.

---

## ⚖️ Handling Class Imbalance

Fraud detection is an extremely imbalanced classification problem.

FraudLens addresses this during model training using:

```python
class_weight="balanced"
```

for the supported classification models.

Evaluation focuses on metrics that are more informative than accuracy alone, particularly:

- Precision
- Recall
- F1 Score
- ROC-AUC
- PR-AUC

---

## 🧪 Model Development

The project includes experimentation with multiple classical machine learning approaches during model development.

The current deployed prediction pipeline uses:

**Random Forest**

The preprocessing workflow also evaluates:

- Logistic Regression
- Decision Tree
- Random Forest

The final model was selected based on fraud-detection performance rather than raw accuracy.

---

## 🛠️ Tech Stack

### Machine Learning

- Python
- pandas
- NumPy
- scikit-learn
- joblib

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

---

## 🔬 Development Workflow

FraudLens was developed incrementally rather than as a single monolithic implementation.

The workflow includes:

```text
Dataset Exploration
        ↓
Preprocessing
        ↓
Model Training
        ↓
Evaluation
        ↓
Threshold Tuning
        ↓
Model Packaging
        ↓
Prediction API
        ↓
API Validation
        ↓
Interactive Frontend
        ↓
Risk Signals
```

This structure keeps experimentation, model development, API development, and frontend integration separated.

---

## ⚠️ Limitations

FraudLens is a portfolio and educational machine learning application and should not be treated as a production financial fraud detection system.

Important limitations include:

- The dataset contains anonymized PCA features.
- The model does not have access to real-world merchant, customer, device, or geographic information.
- Risk signals describe model-relevant statistical patterns rather than business-level fraud causes.
- Model performance depends heavily on the underlying dataset.
- The classification threshold is tuned for this dataset and may not generalize to another transaction population.
- The current model does not continuously retrain itself on new financial data.
- No claim is made that the model can replace professional fraud investigation systems.

---

## 🚀 Future Improvements

Potential future development includes:

- SHAP-based local explanations
- More robust model comparison
- Hyperparameter optimization
- Precision-Recall curve visualization
- Model drift monitoring
- Automated retraining workflows
- Feature distribution monitoring
- More advanced anomaly detection
- Authentication and API security
- Production-grade deployment infrastructure

These are planned improvements rather than currently implemented capabilities.

---

## 🎓 Project Goals

FraudLens was built to demonstrate practical machine learning engineering across the complete lifecycle of a classification system:

```text
Data
→ Preprocessing
→ Imbalanced Classification
→ Model Evaluation
→ Threshold Optimization
→ Model Packaging
→ REST API
→ Frontend Integration
→ Explainability
```

The goal is not only to train a fraud classifier, but to demonstrate how a machine learning model can be turned into an interactive application.

---

## 📄 License

This project is licensed under the MIT License.
