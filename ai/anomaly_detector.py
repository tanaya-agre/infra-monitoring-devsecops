import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest

DB = "/home/admin/AISIMDP/database/monitoring.db"

conn = sqlite3.connect(DB)

df = pd.read_sql_query(
    "SELECT hostname, cpu, memory, disk FROM metrics",
    conn
)

if len(df) >= 10:

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(
        df[["cpu", "memory", "disk"]]
    )

    anomalies = df[
        (df["anomaly"] == -1) &
        (
            (df["cpu"] > 50) |
            (df["memory"] > 70) |
            (df["disk"] > 70)
        )
    ]

    if len(anomalies) > 0:

        for _, row in anomalies.iterrows():

            alert = (
                f"High resource usage - "
                f"CPU: {row['cpu']}%, "
                f"Memory: {row['memory']}%, "
                f"Disk: {row['disk']}%"
            )

            conn.execute(
                "INSERT INTO alerts (hostname, alert) VALUES (?, ?)",
                (row["hostname"], alert)
            )

        conn.commit()

        print("⚠️ Anomaly detected and alert saved!")

    else:
        print("✅ No significant anomalies detected.")

else:
    print("Not enough data.")

conn.close()
