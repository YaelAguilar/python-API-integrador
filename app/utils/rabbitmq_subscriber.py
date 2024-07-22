import pika
import json
from app.config.rabbitmq import get_rabbitmq_connection
from app.controllers.agua_controller import calcular_cantidad_agua
from app.controllers.fertilizante_controller import calcular_cantidad_fertilizante
from app.controllers.tiempo_fertilizante_controller import calcular_tiempo_en_agotar_fertilizante
import time
import datetime

def callback(ch, method, properties, body):
    data = json.loads(body)
    sensor_id = data.get('sensor_id')
    tipo = data.get('tipo')
    cantidad = data.get('cantidad')
    timestamp = data.get('timestamp')
    inicio = data.get('inicio')
    fin = data.get('fin')

    if tipo == 'agua':
        calcular_cantidad_agua(sensor_id, cantidad, timestamp)
    elif tipo == 'fertilizante':
        calcular_cantidad_fertilizante(sensor_id, cantidad, timestamp)
        if inicio and fin:
            calcular_tiempo_en_agotar_fertilizante(sensor_id, inicio, fin)

def start_consuming():
    while True:
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            # Colas a las que se suscribirá
            channel.queue_declare(queue='sensor_data')

            channel.basic_consume(
                queue='sensor_data', on_message_callback=callback, auto_ack=True
            )

            print(' [*] Esperando por mensajes. Para salir presiona CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error de conexión a RabbitMQ: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            print("Reintentando en 5 segundos...")
            time.sleep(5)
