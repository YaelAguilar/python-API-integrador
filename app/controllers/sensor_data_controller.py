from flask import jsonify
from app.models.consumo_agua import ConsumoAgua
from app.models.consumo_fertilizante import ConsumoFertilizante
from app.models.estado_planta import EstadoPlanta
from app.models.lectura_sensor import LecturaSensor

def obtener_consumo_agua():
    consumos = ConsumoAgua.query.all()
    resultados = [{'consumo_id': c.consumo_id, 'sensor_id': c.sensor_id, 'cantidad': c.cantidad} for c in consumos]
    return jsonify(resultados), 200

def obtener_consumo_fertilizante():
    consumos = ConsumoFertilizante.query.all()
    resultados = [{'consumo_id': c.consumo_id, 'sensor_id': c.sensor_id, 'cantidad': c.cantidad} for c in consumos]
    return jsonify(resultados), 200

def obtener_estado_planta():
    estados = EstadoPlanta.query.all()
    resultados = [{'estado_id': e.estado_id, 'temperatura': e.temperatura, 'conductividad': e.conductividad, 'humedad': e.humedad} for e in estados]
    return jsonify(resultados), 200

def obtener_lecturas_sensor():
    lecturas = LecturaSensor.query.all()
    resultados = [{'lectura_id': l.lectura_id, 'sensor_id': l.sensor_id, 'valor': l.valor, 'unidad': l.unidad} for l in lecturas]
    return jsonify(resultados), 200
