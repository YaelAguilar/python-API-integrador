from app.models.consumo_agua import ConsumoAgua
from app.models.sensor import Sensor
from app.db import db
from flask import jsonify
from app.utils.websocket_client import send_to_websocket

def calcular_cantidad_agua(sensor_id, cantidad, timestamp):
    print(f"Datos recibidos para agua - Sensor ID: {sensor_id}, Cantidad: {cantidad}, Timestamp: {timestamp}")

    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return jsonify({'mensaje': 'Sensor no encontrado'}), 400

    consumo = ConsumoAgua(sensor_id=sensor_id, cantidad=cantidad, timestamp=timestamp)
    db.session.add(consumo)
    db.session.commit()
    print(f"Agua consumida registrada: Sensor ID {sensor_id}, Cantidad {cantidad} litros")

    send_to_websocket('flujoAgua', {'sensor_id': sensor_id, 'cantidad': cantidad, 'timestamp': timestamp})

    return jsonify({'mensaje': 'Consumo de agua registrado exitosamente'}), 201
