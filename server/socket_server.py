import socket
import json
import sqlite3
import os

HOST = "0.0.0.0"
PORT = 9999

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "..", "database", "monitoring.db")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print("Server started...")
print("Waiting for connection...\n")

while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    try:
        data = conn.recv(4096).decode()

        if data:
            metrics = json.loads(data)

            print(metrics)

            con = sqlite3.connect(DB)
            cur = con.cursor()

            cur.execute("""
                INSERT INTO metrics
                (hostname, cpu, memory, disk, network_sent, network_received)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                metrics["hostname"],
                metrics["cpu"],
                metrics["memory"],
                metrics["disk"],
                metrics["network_sent"],
                metrics["network_received"]
            ))

            con.commit()
            con.close()

            print("Saved to Database\n")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()

