import pika
import json
import time
from app.config.rabbitmq import get_rabbitmq_connection
from flask import current_app
from app.db import db
from app.models.consumo_agua import ConsumoAgua
from app.models.consumo_fertilizante import ConsumoFertilizante
from app.models.estado_planta import EstadoPlanta
from app.models.lectura_sensor import LecturaSensor
from app.models.sensor import Sensor

def callback(ch, method, properties, body):
    current_app.logger.info(f"Mensaje recibido: {body}")
    try:
        data = json.loads(body)
        current_app.logger.info(f"Datos decodificados: {data}")

        # Procesar flujo de agua
        if 'litrosPorMinuto' in data and 'totalConsumido' in data:
            sensor = Sensor.query.filter_by(tipo="Sensor_agua").first()
            if sensor:
                consumo_agua = ConsumoAgua(sensor_id=sensor.sensor_id, cantidad=data['totalConsumido'])
                db.session.add(consumo_agua)
                db.session.commit()
                current_app.logger.info(f"Registro guardado en la tabla ConsumoAgua: {data}")

        # Procesar nivel de agua
        elif 'sensorState' in data:
            sensor = Sensor.query.filter_by(tipo="Sensor_agua").first()
            if sensor:
                lectura_sensor = LecturaSensor(sensor_id=sensor.sensor_id, valor=1 if data['sensorState'] == 'hay agua' else 0, unidad='estado')
                db.session.add(lectura_sensor)
                db.session.commit()
                current_app.logger.info(f"Registro guardado en la tabla LecturaSensor para nivelAgua: {data}")

        # Procesar nivel de fertilizante
        elif 'sensorState' in data:
            sensor = Sensor.query.filter_by(tipo="sensor_fertilizante").first()
            if sensor:
                lectura_sensor = LecturaSensor(sensor_id=sensor.sensor_id, valor=1 if data['sensorState'] == 'hay fertilizante' else 0, unidad='estado')
                db.session.add(lectura_sensor)
                db.session.commit()
                current_app.logger.info(f"Registro guardado en la tabla LecturaSensor para nivelFertilizante: {data}")

        # Procesar pH
        elif 'humedad' in data and 'temperatura' in data and 'conductividad' in data:
            estado_planta = EstadoPlanta(humedad=data['humedad'], temperatura=data['temperatura'], conductividad=data['conductividad'])
            db.session.add(estado_planta)
            db.session.commit()
            current_app.logger.info(f"Registro guardado en la tabla EstadoPlanta: {data}")

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
