from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay, confusion_matrix

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "creditcard.csv"
OUT = ROOT / "docs" / "plots"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    if not DATA.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA}")

    df = pd.read_csv(DATA)
    if "Class" not in df:
        raise ValueError("Dataset must contain a Class column")

    if "fraud_probability" not in df or "prediction" not in df:
        raise ValueError("Add model predictions before generating evaluation plots")

    y = df["Class"]
    p = df["fraud_probability"]
    pred = df["prediction"]

    RocCurveDisplay.from_predictions(y, p)
    plt.tight_layout()
    plt.savefig(OUT / "roc_curve.png", dpi=180)
    plt.close()

    PrecisionRecallDisplay.from_predictions(y, p)
    plt.tight_layout()
    plt.savefig(OUT / "precision_recall_curve.png", dpi=180)
    plt.close()

    cm = confusion_matrix(y, pred)
    ConfusionMatrixDisplay(cm, display_labels=["Legitimate", "Fraud"]).plot()
    plt.tight_layout()
    plt.savefig(OUT / "confusion_matrix.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    main()
