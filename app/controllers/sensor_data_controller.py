from flask import jsonify
from app.models.consumo_agua import ConsumoAgua
from app.models.consumo_fertilizante import ConsumoFertilizante
from app.models.estado_planta import EstadoPlanta
from app.models.lectura_sensor import LecturaSensor

def obtener_consumo_agua():
    try:
        consumos = ConsumoAgua.query.all()
        datos = [{"consumo_id": consumo.consumo_id, "sensor_id": consumo.sensor_id, "cantidad": consumo.cantidad, "litros_por_minuto": consumo.litros_por_minuto} for consumo in consumos]
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obtener_consumo_fertilizante():
    try:
        consumos = ConsumoFertilizante.query.all()
        datos = [{"consumo_id": consumo.consumo_id, "sensor_id": consumo.sensor_id, "cantidad": consumo.cantidad} for consumo in consumos]
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obtener_estado_planta():
    try:
        estados = EstadoPlanta.query.all()
        datos = [{"estado_id": estado.estado_id, "humedad": estado.humedad, "temperatura": estado.temperatura, "conductividad": estado.conductividad} for estado in estados]
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def obtener_lecturas_sensor():
    try:
        lecturas = LecturaSensor.query.all()
        datos = [{"lectura_id": lectura.lectura_id, "sensor_id": lectura.sensor_id, "valor": lectura.valor, "unidad": lectura.unidad} for lectura in lecturas]
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
