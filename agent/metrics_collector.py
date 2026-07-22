import psutil
import socket
import time
import json
from datetime import datetime

def get_system_metrics():
    """Collects current system health metrics and returns them as a dictionary."""

    cpu_percent = psutil.cpu_percent(interval=1)          # % CPU used right now
    memory = psutil.virtual_memory()                      # RAM stats
    disk = psutil.disk_usage('/')                         # Disk stats for root partition
    net = psutil.net_io_counters()                         # Network bytes sent/received

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

if __name__ == "__main__":
    while True:
        data = get_system_metrics()
        print(data)
        log_metrics(data)
        time.sleep(5)

if __name__ == "__main__":
    while True:
        data = get_system_metrics()
        print(data)
        time.sleep(5)   # collect every 5 seconds
