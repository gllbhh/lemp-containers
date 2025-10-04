from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )

@app.get('/api/health')
def health():
    return {'status': 'ok'}

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 'This message is rendered by database but is not stored in it!'")
        (msg,) = cur.fetchone()
        return jsonify(message=msg)
    finally:
        cur.close()
        conn.close()

@app.get('/api/time')
def get_time():
    """Return MySQL server time (NOW()) as ISO-8601."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT NOW()")
        (now_val,) = cur.fetchone()  # MySQL DATETIME → Python datetime
        # Convert to string for JSON; ISO 8601 keeps it readable and sortable.
        return jsonify(time=now_val.isoformat())
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    # Dev-only fallback
    app.run(host='0.0.0.0', port=8000, debug=True)
