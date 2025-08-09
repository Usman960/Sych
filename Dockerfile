# slim is a much smaller image than python:3.11 which comes with many dev tools pre installed
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# --no-cache-dir flag prevents pip from keeping .whl and .tar.gz files in its local cache dir
# further reducing the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
