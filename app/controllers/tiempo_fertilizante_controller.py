from flask import jsonify
import datetime

def calcular_tiempo_en_agotar_fertilizante(sensor_id, inicio, fin):
    inicio_dt = datetime.datetime.fromisoformat(inicio)
    fin_dt = datetime.datetime.fromisoformat(fin)
    
    tiempo = (fin_dt - inicio_dt).total_seconds()
    
    return jsonify({'mensaje': 'Tiempo en agotar fertilizante calculado', 'tiempo': tiempo}), 201
