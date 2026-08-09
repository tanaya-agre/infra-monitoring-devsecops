FROM python:3.11-slim

WORKDIR /app

COPY dashboard/requirements-dashboard.txt .
RUN pip install --no-cache-dir -r requirements-dashboard.txt

COPY dashboard/ ./dashboard/
COPY database/ ./database/

RUN mkdir -p /app/logs

EXPOSE 5000

WORKDIR /app/dashboard
CMD ["python", "app.py"]
