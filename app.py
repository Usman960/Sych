from flask import Flask, request
from threading import Thread
from mock import mock_model_predict
from queue import Queue
import uuid

app = Flask(__name__)

queue = Queue()
results = {}

def worker():
    while True:
        input, predictionId = queue.get()
        result = mock_model_predict(input)
        results[predictionId] = result
        queue.task_done()

thread = Thread(target=worker, daemon=True)
thread.start()

@app.route("/predict", methods=['POST'])
def predict():
    isAsync = request.headers.get("Async-Mode")
    input = request.get_json().get("input")

    if isAsync:
        predictionId = str(uuid.uuid4())
        results[predictionId] = None
        queue.put((input, predictionId))
        return {"message": "Request received. Processing asynchronously.",
                "prediction_id": predictionId}, 202
    else:
        return mock_model_predict(input)

@app.route("/predict/<predictionId>", methods=['GET'])
def getResults(predictionId):
    if predictionId in results:
        result = results[predictionId]
        if result is None:
            return {"error": "Prediction is still being processed."}, 400
        else:
            return {
                "prediction_id": predictionId,
                "output": result
            }
    else:
        return {"error": "Prediction ID not found."}, 404

if __name__ == '__main__':
    app.run(port=8080)

