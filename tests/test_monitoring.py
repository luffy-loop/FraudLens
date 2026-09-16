import pytest

from monitoring.prediction_monitor import population_shift, summarize_predictions


def test_summary():
    s = summarize_predictions([0.1, 0.7, 0.9, 0.2], 0.6)
    assert s.total == 4
    assert s.fraud_count == 2
    assert s.legitimate_count == 2
    assert s.fraud_rate == 0.5
    assert s.mean_probability == 0.475


def test_summary_rejects_empty():
    with pytest.raises(ValueError):
        summarize_predictions([], 0.6)


def test_summary_rejects_invalid_probability():
    with pytest.raises(ValueError):
        summarize_predictions([1.2], 0.6)


def test_summary_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        summarize_predictions([0.2], 1.1)


def test_population_shift():
    assert population_shift([0.1, 0.2], [0.4, 0.5]) == 0.3


def test_population_shift_rejects_empty():
    with pytest.raises(ValueError):
        population_shift([], [0.1])
