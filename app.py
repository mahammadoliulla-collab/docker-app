import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "appdb")),
        user=os.getenv("DB_USER", os.getenv("POSTGRES_USER", "postgres")),
        password=os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD", "postgres"))
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from a containerized Flask app!",
        "environment": os.getenv("APP_ENV", "development")
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/init")
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS visits ("
        "id SERIAL PRIMARY KEY, ts TIMESTAMP NOT NULL);"
    )
    conn.commit()
    cur.close()
    conn.close()
    return "database initialized"


@app.route("/count")
def count():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO visits (ts) VALUES (NOW()); "
        "SELECT COUNT(*) FROM visits;"
    )
    n = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(total_visits=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
