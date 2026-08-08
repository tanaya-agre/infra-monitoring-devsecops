FROM python:3.11-slim
WORKDIR /app
COPY dashboard/ ./dashboard/
COPY database/ ./database/
RUN pip install flask
EXPOSE 5000
WORKDIR /app/dashboard
CMD ["python3", "app.py"]
