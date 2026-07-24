import psutil
import socket
import socket as sock_module
import time
import json
from datetime import datetime

def get_system_metrics():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    metrics = {
        "hostname": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_used_mb": round(memory.used / (1024 * 1024), 2),
        "memory_total_mb": round(memory.total / (1024 * 1024), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "network_bytes_sent": net.bytes_sent,
        "network_bytes_recv": net.bytes_recv,
    }
    return metrics

LOG_FILE = "../logs/agent_metrics.log"

def log_metrics(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999

def send_to_server(data):
    try:
        client_socket = sock_module.socket(sock_module.AF_INET, sock_module.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        client_socket.sendall(json.dumps(data).encode("utf-8"))
        client_socket.close()
        print("Sent to server successfully.")
    except ConnectionRefusedError:
        print("Could not reach server — is socket_server.py running?")

if __name__ == "__main__":
    while True:
        data = get_system_metrics()
        print(data)
        log_metrics(data)
        send_to_server(data)
        time.sleep(5)
