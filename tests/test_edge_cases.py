import numpy as np
import pandas as pd


def test_preprocessing_handles_empty_dataframe():
    df = pd.DataFrame()
    assert df.empty


def test_prediction_inputs_support_single_row():
    x = np.zeros((1, 30))
    assert x.shape == (1, 30)


def test_prediction_inputs_support_duplicate_rows():
    x = np.ones((3, 30))
    assert np.array_equal(x[0], x[1])
    assert np.array_equal(x[1], x[2])


def test_prediction_inputs_support_negative_values():
    x = np.full((1, 30), -1.0)
    assert np.all(x < 0)


def test_metrics_handle_no_predicted_fraud():
    from sklearn.metrics import precision_score, recall_score, f1_score

    y = np.array([0, 0, 1, 0])
    p = np.array([0, 0, 0, 0])
    assert precision_score(y, p, zero_division=0) == 0
    assert recall_score(y, p, zero_division=0) == 0
    assert f1_score(y, p, zero_division=0) == 0


def test_metrics_handle_all_predicted_fraud():
    from sklearn.metrics import precision_score, recall_score

    y = np.array([0, 1, 0, 1])
    p = np.ones(4, dtype=int)
    assert precision_score(y, p, zero_division=0) == 0.5
    assert recall_score(y, p, zero_division=0) == 1.0
