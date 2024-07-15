import pika
import json
from app.config.rabbitmq import get_rabbitmq_connection
from app.controllers.agua_controller import calcular_cantidad_agua
from app.controllers.fertilizante_controller import calcular_cantidad_fertilizante

def callback(ch, method, properties, body):
    data = json.loads(body)
    sensor_id = data['sensor_id']
    tipo = data['tipo']
    cantidad = data['cantidad']
    timestamp = data['timestamp']

    if tipo == 'agua':
        calcular_cantidad_agua(sensor_id, cantidad)
    elif tipo == 'fertilizante':
        calcular_cantidad_fertilizante(sensor_id, cantidad)

def start_consuming():
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # colas a las que se suscribirá
    channel.queue_declare(queue='sensor_data')

    channel.basic_consume(
        queue='sensor_data', on_message_callback=callback, auto_ack=True
    )

    print(' [*] Esperando por mensajes. Para salir presiona CTRL+C')
    channel.start_consuming()
