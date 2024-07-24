from threading import Thread
import pika
import json
import time
import random
from app.config.rabbitmq import get_rabbitmq_connection
from flask import current_app
from app.db import db
from app.models.consumo_agua import ConsumoAgua
from app.models.estado_planta import EstadoPlanta
from app.models.sensor import Sensor

def callback(ch, method, properties, body):
    current_app.logger.info(f"Mensaje recibido: {body}")
    try:
        data = json.loads(body)
        current_app.logger.info(f"Datos decodificados: {data}")

        # Procesar flujo de agua
        if 'litrosPorMinuto' in data and 'totalConsumido' in data:
            sensor = Sensor.query.filter_by(tipo="sensor_agua").first()
            if sensor:
                consumo_agua = ConsumoAgua(sensor_id=sensor.sensor_id, cantidad=data['totalConsumido'], litros_por_minuto=data['litrosPorMinuto'])
                db.session.add(consumo_agua)
                db.session.commit()
                current_app.logger.info(f"Registro guardado en la tabla ConsumoAgua: {data}")
                print(f"Datos simulados guardados en ConsumoAgua: {data}")

        # Procesar pH
        elif 'humedad' in data and 'temperatura' in data and 'conductividad' in data:
            estado_planta = EstadoPlanta(humedad=data['humedad'], temperatura=data['temperatura'], conductividad=data['conductividad'])
            db.session.add(estado_planta)
            db.session.commit()
            current_app.logger.info(f"Registro guardado en la tabla EstadoPlanta: {data}")
            print(f"Datos simulados guardados en EstadoPlanta: {data}")

    except json.JSONDecodeError:
        current_app.logger.error(f"Error al decodificar el JSON: {body}")
    except Exception as e:
        current_app.logger.error(f"Error al procesar el mensaje: {e}")

def simulate_data():
    while True:
        try:
            data_flujo_agua = {
                'litrosPorMinuto': random.uniform(0.1, 10.0),
                'totalConsumido': random.uniform(0.1, 100.0)
            }
            data_ph = {
                'humedad': random.uniform(30.0, 70.0),
                'temperatura': random.uniform(10.0, 35.0),
                'conductividad': random.uniform(0.1, 5.0)
            }
            print(f"Simulando datos de flujo de agua: {data_flujo_agua}")
            print(f"Simulando datos de pH: {data_ph}")

            # Guardar datos simulados en la base de datos
            callback(None, None, None, json.dumps(data_flujo_agua))
            callback(None, None, None, json.dumps(data_ph))

            time.sleep(10)

        except Exception as e:
            print(f"Error al generar datos simulados: {e}")

def start_consuming():
    current_app.logger.info("Iniciando consumo de RabbitMQ")
    simulate_thread = Thread(target=simulate_data)
    simulate_thread.start()
    while True:
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()

            queue_names = ['flujoAgua', 'ph']

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
