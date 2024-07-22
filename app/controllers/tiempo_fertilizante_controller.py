from flask import jsonify
from app.models.consumo_fertilizante import ConsumoFertilizante
from app.db import db
import datetime

def calcular_tiempo_en_agotar_fertilizante(sensor_id, inicio, fin):
    # Convertir las cadenas de fecha en objetos datetime
    inicio_dt = datetime.datetime.fromisoformat(inicio)
    fin_dt = datetime.datetime.fromisoformat(fin)
    
    # Calcular el tiempo en segundos
    tiempo = (fin_dt - inicio_dt).total_seconds()
    
    # Crear un nuevo registro en ConsumoFertilizante con el tiempo calculado
    nuevo_consumo = ConsumoFertilizante(sensor_id=sensor_id, cantidad=0, timestamp=fin_dt)
    
    # Agregar y guardar en la base de datos
    db.session.add(nuevo_consumo)
    db.session.commit()
    
    return jsonify({'mensaje': 'Tiempo en agotar fertilizante calculado', 'tiempo': tiempo}), 201
