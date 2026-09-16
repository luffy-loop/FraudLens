import os
from functools import wraps

from flask import jsonify, request


def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        expected = os.getenv("FRAUDLENS_API_KEY")
        if not expected:
            return jsonify({"error": "API authentication is not configured"}), 503

        supplied = request.headers.get("X-API-Key")
        if supplied != expected:
            return jsonify({"error": "Invalid or missing API key"}), 401

        return fn(*args, **kwargs)

    return wrapper
