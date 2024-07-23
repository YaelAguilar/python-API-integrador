import pika
import json
import time
from app.config.rabbitmq import get_rabbitmq_connection
from flask import current_app
from app.utils.websocket_client import send_to_websocket

def callback(ch, method, properties, body):
    current_app.logger.info(f"Mensaje recibido: {body}")
    try:
        data = json.loads(body)
        current_app.logger.info(f"Datos decodificados: {data}")

        if method.routing_key == 'flujoAgua' and 'flow_rate_lpm' in data and 'total_liters' in data:
            transformed_data = {
                "tipo": "flujoAgua",
                "data": {
                    "litrosPorMinuto": data['flow_rate_lpm'],
                    "totalConsumido": data['total_liters']
                }
            }
        elif method.routing_key == 'nivelAgua' and 'sensor_state' in data:
            transformed_data = {
                "tipo": "nivelAgua",
                "data": {
                    "sensorState": data['sensor_state']
                }
            }
        elif method.routing_key == 'nivelFertilizante' and 'sensor_state' in data:
            transformed_data = {
                "tipo": "nivelFertilizante",
                "data": {
                    "sensorState": data['sensor_state']
                }
            }
        elif method.routing_key == 'ph' and 'humidity' in data and 'temperature' in data and 'conductivity' in data:
            transformed_data = {
                "tipo": "ph",
                "data": {
                    "humedad": data['humidity'],
                    "temperatura": data['temperature'],
                    "conductividad": data['conductivity']
                }
            }
        else:
            current_app.logger.error(f"Datos incompletos o no reconocidos recibidos: {data}")
            return
        
        current_app.logger.info(f"Transformado a: {transformed_data}")
        send_to_websocket(transformed_data['tipo'], transformed_data)
        current_app.logger.info(f"Enviando datos a WebSocket: {transformed_data}")
    except json.JSONDecodeError:
        current_app.logger.error(f"Error al decodificar el JSON: {body}")
    except Exception as e:
        current_app.logger.error(f"Error al procesar el mensaje: {e}")

def start_consuming():
    current_app.logger.info("Iniciando consumo de RabbitMQ")
    while True:
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            queue_names = ['flujoAgua', 'nivelAgua', 'nivelFertilizante', 'ph']

            for queue_name in queue_names:
                current_app.logger.info(f"Suscribiéndose a la cola: {queue_name}")
                channel.queue_declare(queue=queue_name, durable=True)
                channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

            current_app.logger.info(' [*] Esperando por mensajes. Para salir presiona CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            current_app.logger.error(f"Error de conexión a RabbitMQ: {e}")
            current_app.logger.info("Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            current_app.logger.error(f"Ocurrió un error inesperado: {e}")
            current_app.logger.info("Reintentando en 5 segundos...")
            time.sleep(5)
