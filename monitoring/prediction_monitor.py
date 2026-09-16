from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class PredictionSummary:
    total: int
    fraud_count: int
    legitimate_count: int
    fraud_rate: float
    mean_probability: float


def summarize_predictions(probabilities: Iterable[float], threshold: float) -> PredictionSummary:
    p = np.asarray(list(probabilities), dtype=float)
    if p.size == 0:
        raise ValueError("probabilities must not be empty")
    if not np.all(np.isfinite(p)) or np.any((p < 0) | (p > 1)):
        raise ValueError("probabilities must be finite values between 0 and 1")
    if not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    pred = p >= threshold
    fraud_count = int(pred.sum())
    total = int(p.size)

    return PredictionSummary(
        total=total,
        fraud_count=fraud_count,
        legitimate_count=total - fraud_count,
        fraud_rate=round(fraud_count / total, 6),
        mean_probability=round(float(p.mean()), 6),
    )


def population_shift(reference: Iterable[float], current: Iterable[float]) -> float:
    r = np.asarray(list(reference), dtype=float)
    c = np.asarray(list(current), dtype=float)
    if r.size == 0 or c.size == 0:
        raise ValueError("reference and current values must not be empty")
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(c)):
        raise ValueError("values must be finite")
    return round(abs(float(r.mean()) - float(c.mean())), 6)
