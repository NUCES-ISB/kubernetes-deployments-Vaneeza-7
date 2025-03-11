# ---- Stage 1: Builder Image ----
    FROM python:3.9-slim AS builder

    WORKDIR /app
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
    
    FROM python:3.9-slim
    
    WORKDIR /app
    
    # Create a non-root user
    RUN useradd --create-home appuser
    USER appuser
    
    COPY --from=builder /install /usr/local
    
    COPY . .
    
    EXPOSE 5000
    
    CMD ["python", "app.py"]
    