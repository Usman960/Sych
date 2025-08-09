from flask import Flask, request
from threading import Thread
from mock import mock_model_predict
import uuid
from typing import Dict, Optional, Any
import json
from rabbitmq import create_rabbitmq_connection

app = Flask(__name__)

connection, channel = create_rabbitmq_connection() # create a connection and channel for flask (main) thread

# temporarily stores prediction results
results: Dict[str, Optional[Dict[str, str]]] = {} # value can be either the dict returned from mock_model_predict 
                                                  # or None

# this is the background thread which will consume tasks from queue
def rabbitmq_worker() -> None:
    connection, channel = create_rabbitmq_connection() # create a connection and channel for worker thread

    def callback(ch, method, properties, body):
        task = json.loads(body) # convert the json body back to python dictionary
        prediction_id = task['prediction_id']
        input_value = task['input']

        result = mock_model_predict(input_value)
        results[prediction_id] = result # store the return value from mock_model_predict against the prediction key
    
    channel.basic_consume(queue='prediction_tasks', on_message_callback=callback, auto_ack=True) # start consuming
    channel.start_consuming()

# endpoint for invoking mock_model_predict synchronously/asynchronously
@app.route("/predict", methods=['POST'])
def predict() -> Any:
    isAsync: Optional[str] = request.headers.get("Async-Mode") # extract the value of header
    input: str = request.get_json().get("input") # extract the value of the key 'input' from req body

    # if asynchronous
    if isAsync and isAsync.lower() == "true":
        predictionId: str = str(uuid.uuid4()) # generate a unique prediction id
        results[predictionId] = None    # create an entry in results dict with value set to null
        message = json.dumps({"input": input, "prediction_id": predictionId}) # convert python dictionary to json
        channel.basic_publish(exchange='', routing_key='prediction_tasks', body=message) # publish to queue
        return {"message": "Request received. Processing asynchronously.",
                "prediction_id": predictionId}, 202
    else:
        return mock_model_predict(input) # if synchronous then simply call mock_model_predict

# endpoint to fetch prediction result based on prediction id
@app.route("/predict/<predictionId>", methods=['GET'])
def getResults(predictionId: str) -> Any:
    if predictionId in results:     # first check if the prediction id is present in results dict or not 
        result = results[predictionId]
        if result is None:  # if the prediction id is found but the value is null then the worker is processing it
            return {"error": "Prediction is still being processed."}, 400
        else:   # if a non null value is found then return this along with prediction id
            return {
                "prediction_id": predictionId,
                "output": result
            }
    else:   # return error 404 if prediction id not found in results dict
        return {"error": "Prediction ID not found."}, 404

if __name__ == '__main__':
    Thread(target=rabbitmq_worker, daemon=True).start() # daemon=True means this is a background thread
    app.run(host="0.0.0.0", port=8080)  # ensure the app runs on port 8080 and is accessible from all IP addresses

