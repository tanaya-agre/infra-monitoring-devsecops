import sqlite3

conn = sqlite3.connect("monitoring.db")
cursor = conn.cursor()

# Create Metrics Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT,
    cpu REAL,
    memory REAL,
    disk REAL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Create Alerts Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT,
    alert TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")
