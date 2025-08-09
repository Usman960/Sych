# Stage 1: Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies into a separate directory (/install)
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Stage 2: Final runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed python packages from builder
COPY --from=builder /install /usr/local

# Copy app source code
COPY --from=builder /app /app

EXPOSE 8080

CMD ["python", "app.py"]
