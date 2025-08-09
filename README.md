# Flaskulator – Calculator Web App

A simple **web-based calculator** built with Flask, supporting basic arithmetic operations (**addition, subtraction, multiplication**) with calculation history stored locally for persistence.

---

## 🚀 Features
- Perform basic arithmetic (+, −, ×) via a clean web interface
- Clickable number & operator buttons – no typing needed
- Calculation history is **saved in local files** (`data/` folder)
- Dockerized for quick setup and portability

---

## 🐳 Running with Docker

### 1️⃣ Build the Docker image
```sh
docker build -t flaskulator .
```

### 2️⃣ Run the container
```sh
docker run -p 8090:8090 -v $(pwd)/data:/data flaskulator
```

- The app will be available at [http://localhost:8090](http://localhost:8090)
- Calculation history is persisted in the `data/` directory.

---

## 📄 Example Dockerfile
If you don’t have a `Dockerfile`, use the following:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY calculator.py /app/
RUN pip install flask

EXPOSE 8090
CMD ["python", "calculator.py"]
```

---

## 📝 Notes
- Ensure the `data/` directory exists and is writable for history persistence.
- Stop the container with `Ctrl+C` or `docker stop <container_id>`.
