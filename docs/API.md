# FraudLens API

FraudLens exposes a Flask REST API for transaction scoring.

## Base URL

For local development:

```text
http://localhost:5000
```

## Health Check

```http
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

## Single Prediction

```http
POST /predict
Content-Type: application/json
```

The request must contain these 30 numeric features:

```text
Time, V1, V2, V3, V4, V5, V6, V7, V8, V9,
V10, V11, V12, V13, V14, V15, V16, V17, V18, V19,
V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount
```

Example request:

```json
{
  "Time": 0,
  "V1": -1.36,
  "V2": -0.07,
  "V3": 2.54,
  "V4": 1.38,
  "V5": -0.34,
  "V6": 0.46,
  "V7": 0.24,
  "V8": 0.10,
  "V9": 0.36,
  "V10": 0.09,
  "V11": -0.55,
  "V12": -0.62,
  "V13": -0.99,
  "V14": -0.31,
  "V15": 1.47,
  "V16": -0.47,
  "V17": 0.21,
  "V18": 0.03,
  "V19": 0.40,
  "V20": 0.25,
  "V21": -0.02,
  "V22": 0.28,
  "V23": -0.11,
  "V24": 0.07,
  "V25": 0.13,
  "V26": -0.19,
  "V27": 0.01,
  "V28": -0.02,
  "Amount": 149.62
}
```

Response fields include:

- `fraud_probability`
- `threshold`
- `prediction`
- `result`
- `risk_signals`

## Batch Prediction

```http
POST /predict_batch
Content-Type: application/json
```

Request format:

```json
{
  "transactions": [
    { "Time": 0, "V1": 0, "V2": 0, "V3": 0, "V4": 0, "V5": 0, "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0, "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0, "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0, "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0, "V26": 0, "V27": 0, "V28": 0, "Amount": 0 }
  ]
}
```

The API accepts up to 100 transactions per request.

## Validation

Requests are rejected when:

- required features are missing
- feature values are not finite numbers
- the batch is empty
- the batch exceeds 100 transactions

Errors are returned as JSON with HTTP 400 status codes for invalid input.
