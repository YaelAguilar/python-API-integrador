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
