# Model Comparison

FraudLens evaluates multiple binary classifiers on the same fraud-detection task. Because the dataset is highly imbalanced, accuracy is not used as the primary selection signal.

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 5.64% | 87.37% | 10.59% | 96.56% | 67.19% |
| Decision Tree | 6.83% | 83.16% | 12.62% | 91.48% | 46.96% |
| Random Forest | 77.66% | 76.84% | 77.25% | 97.46% | 78.22% |

## Final operating point

The packaged Random Forest model uses a fraud-probability threshold of **0.60**. At the documented evaluation operating point, the reported metrics are:

- Precision: 86.59%
- Recall: 74.74%
- F1: 80.23%
- ROC-AUC: 97.46%

The threshold is configurable during model development because fraud detection involves a precision/recall trade-off. The historical notebook output at threshold 0.65 is retained as a historical artifact and is not the current packaged threshold.

## Why these metrics matter

Fraud labels are rare, so a model can achieve high accuracy while missing useful fraud signals. Precision measures how many flagged transactions were actually fraud in the evaluation set, while recall measures how much of the observed fraud was detected. PR-AUC summarizes precision-recall behavior across thresholds and is particularly informative for rare positive classes.

These measurements are dataset-specific evaluation results, not guarantees of production performance.
