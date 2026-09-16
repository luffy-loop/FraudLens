# FraudLens Model Card

## Model Identity

| Field | Value |
|---|---|
| Model | Random Forest Classifier |
| Version | v1.0 |
| Features | 30 |
| Threshold | 0.60 |
| Task | Binary credit-card fraud classification |
| Explainability | SHAP + model-driven risk signals |
| Monitoring | Prediction and probability-shift utilities |
| API | Flask prediction service |

## Training Data

FraudLens uses the Credit Card Fraud Detection dataset. The project removes duplicate records during preprocessing and keeps the raw dataset out of source control.

## Evaluation

Evaluation uses a held-out test set. The documented operating-point results for the packaged model are:

- Precision: 86.59%
- Recall: 74.74%
- F1: 80.23%
- ROC-AUC: 97.46%

PR-AUC is also reported in the model comparison benchmark because the fraud class is highly imbalanced.

## Intended Use

The model is intended for educational demonstration, portfolio presentation, experimentation, and transaction-risk analysis on data matching the training feature schema.

## Limitations

The anonymized PCA-derived features do not have direct business interpretations. Evaluation results are specific to the dataset and test split and should not be treated as guarantees of production fraud-detection performance. A production deployment would require continuous monitoring, retraining procedures, data-quality controls, access control, and domain validation.

## Decision Threshold

The packaged model classifies a transaction as fraud when its predicted fraud probability is at least 0.60. Changing this threshold changes the precision/recall trade-off and should be evaluated against the operational cost of false positives and false negatives.
