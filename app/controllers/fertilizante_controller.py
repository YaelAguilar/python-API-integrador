from app.models.consumo_fertilizante import ConsumoFertilizante
from app.models.sensor import Sensor
from app.db import db
from flask import jsonify
from app.utils.websocket_client import send_to_websocket

def calcular_cantidad_fertilizante(sensor_id, cantidad, timestamp):
    print(f"Datos recibidos para fertilizante - Sensor ID: {sensor_id}, Cantidad: {cantidad}, Timestamp: {timestamp}")

    sensor = Sensor.query.get(sensor_id)
    if not sensor:
        return jsonify({'mensaje': 'Sensor no encontrado'}), 400

    consumo = ConsumoFertilizante(sensor_id=sensor_id, cantidad=cantidad, timestamp=timestamp)
    db.session.add(consumo)
    db.session.commit()
    print(f"Fertilizante consumido registrado: Sensor ID {sensor_id}, Cantidad {cantidad} litros")

    send_to_websocket('nivelFertilizante', {'sensor_id': sensor_id, 'cantidad': cantidad, 'timestamp': timestamp})

    return jsonify({'mensaje': 'Consumo de fertilizante registrado exitosamente'}), 201
