import os
import pika
import time
import logging

rabbit_host = os.getenv("RABBITMQ_HOST", "localhost")
rabbit_user = os.getenv("RABBITMQ_USER", "guest")
rabbit_pass = os.getenv("RABBITMQ_PASS", "guest")

def create_rabbitmq_connection(retries=10, delay=5):
    credentials = pika.PlainCredentials(rabbit_user, rabbit_pass)
    for attempt in range(1, retries + 1):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=rabbit_host, credentials=credentials)
            )
            channel = connection.channel()
            channel.queue_declare(queue='prediction_tasks')
            print(f"Connected to RabbitMQ on attempt {attempt}")
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning(f"Attempt {attempt} failed to connect to RabbitMQ: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after multiple retries")