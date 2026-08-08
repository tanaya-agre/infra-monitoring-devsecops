import sqlite3

DB = "../database/monitoring.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

cur = conn.cursor()

# Get the latest monitoring record
cur.execute("SELECT * FROM metrics ORDER BY id DESC LIMIT 1")

data = cur.fetchone()

conn.close()

if data:

    print("\n----- Latest Server Status -----")
    print("Hostname :", data["hostname"])
    print("CPU      :", data["cpu"], "%")
    print("Memory   :", data["memory"], "%")
    print("Disk     :", data["disk"], "%")

    print("\n----- Alerts -----")

    alert = False

    if data["cpu"] > 80:
        print("High CPU Usage!")
        alert = True

    if data["memory"] > 80:
        print("High Memory Usage!")
        alert = True

    if data["disk"] > 90:
        print("High Disk Usage!")
        alert = True

    if not alert:
        print("System is Healthy.")

else:
    print("No monitoring data found.")
