import socket
import json
import sqlite3

HOST = "0.0.0.0"
PORT = 9999
DB = "../database/monitoring.db"

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Server started...")
print("Waiting for connection...\n")

while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    data = conn.recv(1024).decode()

    if data:
        metrics = json.loads(data)

        print(metrics)

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute("""
        INSERT INTO metrics(hostname,cpu,memory,disk)
        VALUES(?,?,?,?)
        """, (
            metrics["hostname"],
            metrics["cpu"],
            metrics["memory"],
            metrics["disk"]
        ))

        con.commit()
        con.close()

        print("Saved to Database\n")

    conn.close()
