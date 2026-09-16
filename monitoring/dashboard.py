from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class MonitoringSnapshot:
    total: int
    flagged: int
    legitimate: int
    fraud_rate: float
    mean_probability: float
    reference_mean_probability: float
    probability_shift: float
    drift_status: str


def build_snapshot(
    probabilities: list[float],
    threshold: float,
    reference_mean_probability: float,
    drift_tolerance: float = 0.05,
) -> MonitoringSnapshot:
    if not probabilities:
        raise ValueError("probabilities cannot be empty")
    if not 0 < threshold < 1:
        raise ValueError("threshold must be between 0 and 1")
    if not 0 <= reference_mean_probability <= 1:
        raise ValueError("reference mean probability must be between 0 and 1")
    if drift_tolerance < 0:
        raise ValueError("drift tolerance cannot be negative")
    if any(not isfinite(float(p)) or not 0 <= float(p) <= 1 for p in probabilities):
        raise ValueError("probabilities must be finite values between 0 and 1")

    total = len(probabilities)
    flagged = sum(float(p) >= threshold for p in probabilities)
    legitimate = total - flagged
    mean_probability = sum(float(p) for p in probabilities) / total
    shift = mean_probability - reference_mean_probability
    status = "DRIFT" if abs(shift) > drift_tolerance else "STABLE"

    return MonitoringSnapshot(
        total=total,
        flagged=flagged,
        legitimate=legitimate,
        fraud_rate=flagged / total,
        mean_probability=mean_probability,
        reference_mean_probability=reference_mean_probability,
        probability_shift=shift,
        drift_status=status,
    )
