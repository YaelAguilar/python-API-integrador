import os
import pika
import ssl

def get_rabbitmq_connection():
    url = os.getenv('CLOUDAMQP_URL', 'amqps://vumnphwp:04G37mBLNQfL_i6oM1cfMffWzwOOJifD@shrimp.rmq.cloudamqp.com/vumnphwp')
    params = pika.URLParameters(url)
    
    context = ssl.create_default_context()
    params.ssl_options = pika.SSLOptions(context)

    connection = pika.BlockingConnection(params)
    return connection

try:
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    print("Conexión exitosa a RabbitMQ")
except pika.exceptions.AMQPConnectionError as e:
    print(f"Error de conexión a RabbitMQ: {e}")
