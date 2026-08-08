import psutil
import socket
import json
import time

HOST = "127.0.0.1"
PORT = 9999
LOG_FILE = "../logs/agent_metrics.log"

while True:

    data = {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent
    }

    with open(LOG_FILE, "a") as file:
        file.write(json.dumps(data) + "\n")

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(json.dumps(data).encode())
        client.close()
        print("Data Sent Successfully")

    except Exception as e:
        print("Server is not running:", e)

    time.sleep(5)
