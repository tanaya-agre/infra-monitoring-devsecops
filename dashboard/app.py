import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DB = "/app/database/monitoring.db"


@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM metrics
        ORDER BY id DESC
    """)

    data = cur.fetchall()

    conn.close()

    return render_template("index.html", data=data)


@app.route("/alerts")
def alerts():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM alerts
        ORDER BY id DESC
        LIMIT 1
    """)

    alert = cur.fetchone()

    conn.close()

    if alert:
        return jsonify({
            "alert": True,
            "id": alert["id"],
            "hostname": alert["hostname"],
            "message": alert["alert"],
            "time": alert["time"]
        })

    return jsonify({
        "alert": False
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
