from flask import jsonify
from app.models.ConsumoFertilizante import ConsumoFertilizante
from app.db import db
import datetime

def calcular_tiempo_en_agotar_fertilizante(sensor_id, inicio, fin):
    tiempo = (fin - inicio).total_seconds()
    # Aquí puedes guardar el tiempo en una tabla de análisis o similar
    # Por simplicidad, estamos devolviendo el valor calculado
    #Faltaria ampliar la lógica
    return jsonify({'mensaje': 'Tiempo en agotar fertilizante calculado', 'tiempo': tiempo}), 201
