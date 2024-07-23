from flask import jsonify, current_app

def calcular_cantidad_agua(sensor_id, cantidad):
    if sensor_id is None or cantidad is None:
        current_app.logger.error(f"Datos incompletos recibidos: Sensor ID: {sensor_id}, Cantidad: {cantidad}")
        return jsonify({'mensaje': 'Datos incompletos'}), 400

    current_app.logger.info(f"Datos recibidos para agua - Sensor ID: {sensor_id}, Cantidad: {cantidad}")
    return jsonify({'mensaje': 'Datos de agua procesados exitosamente'}), 201
