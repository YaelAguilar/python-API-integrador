import os
import pika
import time
import ssl
from dotenv import load_dotenv

load_dotenv()

def get_rabbitmq_connection():
    url = os.getenv('CLOUDAMQP_URL')
    params = pika.URLParameters(url)
    
    context = ssl.create_default_context()
    params.ssl_options = pika.SSLOptions(context)

    connection = pika.BlockingConnection(params)
    return connection

def on_message(channel, method_frame, header_frame, body):
    print(f"Mensaje recibido de la cola {method_frame.routing_key}: {body}")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def start_consuming():
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        queue_names = ['flujoAgua', 'nivelAgua', 'nivelFertilizante', 'ph']

        for queue_name in queue_names:
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_consume(queue=queue_name, on_message_callback=on_message)

        print("Esperando mensajes de las colas. Presiona CTRL+C para salir.")
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error de conexión a RabbitMQ: {e}")
        print("Reintentando en 5 segundos...")
        time.sleep(5)
        start_consuming()
    except KeyboardInterrupt:
        print("Interrupción por el usuario, cerrando conexión...")
        if connection and connection.is_open:
            connection.close()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        if connection and connection.is_open:
            connection.close()

if __name__ == '__main__':
    start_consuming()
