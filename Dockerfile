FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY dashboard/ ./dashboard/
COPY database/ ./database/

RUN pip install --no-cache-dir flask

EXPOSE 5000

WORKDIR /app/dashboard

CMD ["python3", "app.py"]
