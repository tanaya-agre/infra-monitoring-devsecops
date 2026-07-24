import sqlite3

DB_FILE = "monitoring.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT,
            timestamp TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            memory_used_mb REAL,
            memory_total_mb REAL,
            disk_percent REAL,
            disk_used_gb REAL,
            disk_total_gb REAL,
            network_bytes_sent INTEGER,
            network_bytes_recv INTEGER,
            received_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_FILE}")

if __name__ == "__main__":
    init_db()
