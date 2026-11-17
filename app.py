import os
from flask import Flask, jsonify

raise RuntimeError("CRITICAL: Missing production config key in v2.0")

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from a containerized Flask app!",
        "environment": os.getenv("APP_ENV", "development")
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)