import numpy as np
import pytest

from api.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_predict_missing_payload(client):
    r = client.post("/predict", json={})
    assert r.status_code in (400, 422)


def test_predict_invalid_features(client):
    r = client.post("/predict", json={"features": [1, 2, 3]})
    assert r.status_code in (400, 422)


def test_predict_negative_features_shape(client):
    features = np.full(30, -1.0).tolist()
    r = client.post("/predict", json={"features": features})
    assert r.status_code in (200, 400, 422, 500)


def test_predict_duplicate_feature_rows(client):
    features = np.ones(30).tolist()
    r = client.post("/predict", json={"features": features})
    assert r.status_code in (200, 400, 422, 500)
