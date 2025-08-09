# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
RUN mkdir -p /data
COPY calculator.py .
ENTRYPOINT ["python", "calculator.py"]

