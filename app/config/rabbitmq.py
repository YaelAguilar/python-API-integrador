import pika
import os

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv('R|ABBITMQ_HOST', 'localhost'))
    )
    return connection
