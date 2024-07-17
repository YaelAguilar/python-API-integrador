import os
import pika
import ssl

def get_rabbitmq_connection():
    url = os.getenv('CLOUDAMQP_URL', 'amqps://vumnphwp:04G37mBLNQfL_i6oM1cfMffWzwOOJifD@shrimp.rmq.cloudamqp.com/vumnphwp')
    params = pika.URLParameters(url)
    
    # Configura SSL
    context = ssl.create_default_context()
    params.ssl_options = pika.SSLOptions(context)

    connection = pika.BlockingConnection(params)
    return connection

def on_message(channel, method_frame, header_frame, body):
    print(f"Mensaje recibido de la cola {method_frame.routing_key}: {body}")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

# Uso del método
try:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Nombres de las colas
    queue_names = ['flujoAgua', 'nivelAgua', 'ph']

    for queue_name in queue_names:
        # Declarar la cola (asegúrate de que la cola esté creada en RabbitMQ)
        channel.queue_declare(queue=queue_name, durable=True)
        # Configura la suscripción para recibir mensajes
        channel.basic_consume(queue=queue_name, on_message_callback=on_message)

    print("Esperando mensajes de las colas. Presiona CTRL+C para salir.")
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print(f"Error de conexión a RabbitMQ: {e}")
except KeyboardInterrupt:
    print("Interrupción por el usuario, cerrando conexión...")
    if connection and connection.is_open:
        connection.close()
