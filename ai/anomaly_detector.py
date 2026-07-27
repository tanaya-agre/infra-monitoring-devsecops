import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import time

DB_FILE = "../database/monitoring.db"
CHECK_INTERVAL = 15   # seconds between anomaly checks
LOOKBACK_ROWS = 50    # how many recent readings to analyze each time

def fetch_recent_metrics(limit=LOOKBACK_ROWS):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(f"""
        SELECT id, hostname, timestamp, cpu_percent, memory_percent, disk_percent
        FROM metrics
        ORDER BY id DESC
        LIMIT {limit}
    """, conn)
    conn.close()
    return df.sort_values("id")   # oldest to newest

def save_alert(hostname, timestamp, metric_type, value, message):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts (hostname, timestamp, metric_type, metric_value, message)
        VALUES (?, ?, ?, ?, ?)
    """, (hostname, timestamp, metric_type, value, message))
    conn.commit()
    conn.close()

def detect_anomalies(df):
    if len(df) < 10:
        print("Not enough data yet to detect anomalies (need at least 10 readings).")
        return

    features = df[["cpu_percent", "memory_percent", "disk_percent"]]

    model = IsolationForest(contamination=0.03, random_state=42)
    df = df.copy()
    df["anomaly"] = model.fit_predict(features)

    anomalies = df[df["anomaly"] == -1]

    if anomalies.empty:
        print(f"[{time.ctime()}] System normal. Checked {len(df)} recent readings.")
    else:
        for _, row in anomalies.iterrows():
            message = (f"Unusual system behavior detected on {row['hostname']} at {row['timestamp']}: "
                       f"CPU={row['cpu_percent']}%, Memory={row['memory_percent']}%, Disk={row['disk_percent']}%")
            print(f"🚨 ALERT: {message}")
            save_alert(row["hostname"], row["timestamp"], "combined", row["cpu_percent"], message)

def run_detector():
    print("AI Anomaly Detector started. Checking every", CHECK_INTERVAL, "seconds...")
    while True:
        df = fetch_recent_metrics()
        detect_anomalies(df)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_detector()
