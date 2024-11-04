from flask import jsonify, current_app

def calcular_cantidad_fertilizante(sensor_id, cantidad):
    if sensor_id is None or cantidad is None:
        current_app.logger.error(f"Datos incompletos recibidos: Sensor ID: {sensor_id}, Cantidad: {cantidad}")
        print("Alerta: Nivel bajo - Datos incompletos recibidos")
        return jsonify({'mensaje': 'Datos incompletos'}), 400

    current_app.logger.info(f"Datos recibidos para fertilizante - Sensor ID: {sensor_id}, Cantidad: {cantidad}")
    
    if cantidad > 100:
        print("Alerta: Nivel perfecto - Cantidad de fertilizante óptima")
    elif 50 <= cantidad <= 100:
        print("Alerta: Nivel normal - Cantidad de fertilizante aceptable")
    else:
        print("Alerta: Nivel bajo - Cantidad de fertilizante insuficiente")
    
    return jsonify({'mensaje': 'Datos de fertilizante procesados exitosamente'}), 201
