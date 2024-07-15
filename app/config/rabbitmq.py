import os
import pika

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        username=os.getenv('RABBITMQ_USER', 'guest'),
        password=os.getenv('RABBITMQ_PASSWORD', 'guest')
    )
    parameters = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    return connection
