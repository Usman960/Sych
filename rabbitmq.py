import os
import pika
import time
import logging

# use default credentials if env vars not set up
rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbit_user = os.getenv("RABBITMQ_USER", "guest")
rabbit_pass = os.getenv("RABBITMQ_PASS", "guest")

# establish a connection with rabbitmq
# added a retry mechanism so that the flask app does not crash
def create_rabbitmq_connection(retries: int =10, delay: int =5):
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    for attempt in range(1, retries + 1):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbit_host, credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue='prediction_tasks') # create queue
            print(f"Connected to RabbitMQ on attempt {attempt}")
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Attempt {attempt} failed to connect to RabbitMQ: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after multiple retries")