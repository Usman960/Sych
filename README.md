# Async Prediction API with Flask and RabbitMQ

This project demonstrates an asynchronous prediction API using Flask and RabbitMQ. It supports both synchronous and asynchronous prediction requests by offloading async tasks to a RabbitMQ queue processed by a background worker.

---

## Overview

- The Flask app exposes two endpoints: one for submitting prediction requests and one for fetching async results.
- Synchronous requests return response only after processing the prediction results.
- Asynchronous requests are placed on a RabbitMQ queue and processed by a background worker thread.
- Results are temporarily stored in-memory and can be fetched later using a unique prediction ID.
- RabbitMQ manages task queuing and delivery, decoupling request handling from prediction processing.

---

## Endpoints

### `POST /predict`

Submit a prediction request.

- **Headers**:
  - `Async-Mode`: `"true"` to process asynchronously, omit or set to `"false"` for synchronous.
- **Body** (JSON):
  ```json
  {
    "input": "Sample input data for the model"
  }
- **Response** (JSON): If `Async-Mode` was omitted or set to something else other than `true`, then the reponse will be
  ```json
  {
    "input": "Sample input data for the model",
    "result": "1234"
  }
- **Response** (JSON): If `Async-Mode` was set to `true`, then response will be
  ```json
  {
    "message": "Request received. Processing asynchronously.",
    "prediction_id": "3a2a52a3-a2fa-4bde-b542-4fdc16a1b80d"
  }

### `GET /predict/{predictionId}`

Fetch prediction results based on prediction id.

- **Response** (JSON): If prediction id is not found in memory, then response wil be
  ```json
  {
    "error": "Prediction ID not found."
  }
- **Response** (JSON): If prediction is still being processed then response will be
  ```json
  {
    "error": "Prediction is still being processed."
  }
- **Response** (JSON): If the prediction results are available, response will be
  ```json
  {
    {
      "output": {
          "input": "Sample input data for the model 2",
          "result": "1367"
      },
      "prediction_id": "3a2a52a3-a2fa-4bde-b542-4fdc16a1b80d"
    }
  }

---

## Prerequisites
- Docker and Docker Compose installed on your machine
- RabbitMQ credentials set as environment variables (or defaults will be used):
  - `RABBITMQ_DEFAULT_USER` (default: `guest`)
  - `RABBITMQ_DEFAULT_PASS` (default: `guest`)
  - `RABBITMQ_HOST` (default: `localhost`)

---

## Running the Project Locally with Docker
1. Clone the repository:
   ```bash
   git clone https://github.com/Usman960/Sych.git
   cd Sych
2. Create a `.env` file to set RabbitMQ credentials (optional):
   ```bash
   RABBITMQ_DEFAULT_USER=guest
   RABBITMQ_DEFAULT_PASS=guest
   RABBITMQ_HOST=rabbitmq
3. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
4. Access the services:
   - Flask API: `http://localhost:8080`
   - RabbitMQ Management UI: `http://localhost:15672` 
     (Login with credentials defined in `.env`, defaults are `guest`/`guest`)

