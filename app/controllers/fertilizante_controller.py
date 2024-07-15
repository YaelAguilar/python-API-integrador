from flask import jsonify
from app.models.ConsumoFertilizante import ConsumoFertilizante
from app.db import db
import datetime

def calcular_cantidad_fertilizante(sensor_id, cantidad):
    nuevo_consumo = ConsumoFertilizante(
        sensor_id=sensor_id,
        cantidad=cantidad,
        timestamp=datetime.datetime.utcnow()
    )
    db.session.add(nuevo_consumo)
    db.session.commit()
    return jsonify({'mensaje': 'Consumo de fertilizante registrado exitosamente'}), 201
