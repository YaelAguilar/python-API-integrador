from flask import Blueprint, request, jsonify
from app.controllers.agua_controller import calcular_cantidad_agua
from app.controllers.fertilizante_controller import calcular_cantidad_fertilizante
from app.controllers.crecimiento_controller import CrecimientoPlantaController
from app.controllers.sensor_data_controller import (
    obtener_consumo_agua, obtener_consumo_fertilizante, obtener_estado_planta, obtener_lecturas_sensor
)

sensor_bp = Blueprint('sensor', __name__)

# Rutas GET

@sensor_bp.route('/lecturas_sensor', methods=['GET'])
def get_lecturas_sensor():
    return obtener_lecturas_sensor()

@sensor_bp.route('/consumo_agua', methods=['GET'])
def get_consumo_agua():
    return obtener_consumo_agua()

@sensor_bp.route('/consumo_fertilizante', methods=['GET'])
def get_consumo_fertilizante():
    return obtener_consumo_fertilizante()

@sensor_bp.route('/estado_planta', methods=['GET'])
def get_estado_planta():
    return obtener_estado_planta()

@sensor_bp.route('/crecimiento_planta', methods=['GET'])
def get_all_crecimiento_planta():
    plantas = CrecimientoPlantaController.get_all()
    return jsonify(plantas), 200

@sensor_bp.route('/crecimiento_planta/<int:id>', methods=['GET'])
def get_crecimiento_planta(id):
    planta = CrecimientoPlantaController.get_by_id(id)
    if planta:
        return jsonify(planta), 200
    return jsonify({'mensaje': 'Registro no encontrado'}), 404

# Rutas POST

@sensor_bp.route('/crecimiento_planta', methods=['POST'])
def create_crecimiento_planta():
    datos = request.json
    altura = datos.get('altura')
    if altura is not None:
        nueva_planta = CrecimientoPlantaController.create(altura)
        return jsonify(nueva_planta), 201
    return jsonify({'mensaje': 'Datos insuficientes'}), 400

@sensor_bp.route('/agua', methods=['POST'])
def registrar_agua():
    datos = request.json
    sensor_id = datos.get('sensor_id')
    cantidad = datos.get('cantidad')
    litros_por_minuto = datos.get('litros_por_minuto')
    calcular_cantidad_agua(sensor_id, cantidad, litros_por_minuto)
    return jsonify({'mensaje': 'Datos de agua procesados exitosamente'}), 201

@sensor_bp.route('/fertilizante', methods=['POST'])
def registrar_fertilizante():
    datos = request.json
    sensor_id = datos.get('sensor_id')
    cantidad = datos.get('cantidad')
    calcular_cantidad_fertilizante(sensor_id, cantidad)
    return jsonify({'mensaje': 'Datos de fertilizante procesados exitosamente'}), 201