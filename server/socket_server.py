import socket
import json
import sqlite3
import sys
import os

HOST = "0.0.0.0"      # listen on all network interfaces
PORT = 9999            # port the agent will connect to
DB_FILE = "../database/monitoring.db"

def save_to_db(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metrics (
            hostname, timestamp, cpu_percent, memory_percent,
            memory_used_mb, memory_total_mb, disk_percent,
            disk_used_gb, disk_total_gb, network_bytes_sent, network_bytes_recv
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["hostname"], data["timestamp"], data["cpu_percent"], data["memory_percent"],
        data["memory_used_mb"], data["memory_total_mb"], data["disk_percent"],
        data["disk_used_gb"], data["disk_total_gb"], data["network_bytes_sent"], data["network_bytes_recv"]
    ))
    conn.commit()
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Socket server listening on {HOST}:{PORT} ...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection received from {addr}")
        try:
            raw_data = conn.recv(4096).decode("utf-8")
            if raw_data:
                data = json.loads(raw_data)
                print(f"Received: {data}")
                save_to_db(data)
                print("Saved to database.")
        except Exception as e:
            print(f"Error handling connection: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    start_server()
