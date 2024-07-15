from flask import jsonify
from app.models.ConsumoAgua import ConsumoAgua
from app.db import db
import datetime

def calcular_cantidad_agua(sensor_id, cantidad):
    nuevo_consumo = ConsumoAgua(
        sensor_id=sensor_id,
        cantidad=cantidad,
        timestamp=datetime.datetime.utcnow()
    )
    db.session.add(nuevo_consumo)
    db.session.commit()
    return jsonify({'mensaje': 'Consumo de agua registrado exitosamente'}), 201
