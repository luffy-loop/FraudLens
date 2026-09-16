import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score


def test_empty_arrays_are_supported():
    y = np.array([], dtype=int)
    p = np.array([], dtype=int)
    assert y.size == 0
    assert p.size == 0


def test_single_sample_metrics():
    y = np.array([1])
    p = np.array([1])
    assert precision_score(y, p, zero_division=0) == 1.0
    assert recall_score(y, p, zero_division=0) == 1.0
    assert f1_score(y, p, zero_division=0) == 1.0


def test_duplicate_samples_produce_expected_confusion_matrix():
    y = np.array([0, 0, 1, 1, 1])
    p = np.array([0, 0, 1, 1, 1])
    assert np.array_equal(confusion_matrix(y, p), np.array([[2, 0], [0, 3]]))


def test_reversed_predictions_preserve_recall_precision_behavior():
    y = np.array([0, 0, 1, 1])
    p = np.array([1, 1, 0, 0])
    assert recall_score(y, p, zero_division=0) == 0.0
    assert precision_score(y, p, zero_division=0) == 0.0


def test_negative_feature_values_remain_finite():
    x = np.full((2, 30), -1.0)
    assert np.isfinite(x).all()


def test_missing_fraud_predictions_do_not_raise():
    y = np.array([0, 0, 1, 0])
    p = np.array([0, 0, 0, 0])
    assert recall_score(y, p, zero_division=0) == 0.0


def test_all_fraud_predictions_have_full_recall_when_fraud_exists():
    y = np.array([0, 1, 0, 1])
    p = np.ones(4, dtype=int)
    assert recall_score(y, p, zero_division=0) == 1.0
