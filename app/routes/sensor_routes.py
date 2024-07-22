from flask import Blueprint, request, jsonify
from app.controllers.agua_controller import calcular_cantidad_agua
from app.controllers.fertilizante_controller import calcular_cantidad_fertilizante

sensor_bp = Blueprint('sensor', __name__)

@sensor_bp.route('/agua', methods=['POST'])
def registrar_agua():
    datos = request.json
    sensor_id = datos.get('sensor_id')
    cantidad = datos.get('cantidad')
    timestamp = datos.get('timestamp')
    calcular_cantidad_agua(sensor_id, cantidad, timestamp)
    return jsonify({'mensaje': 'Consumo de agua registrado exitosamente'}), 201

@sensor_bp.route('/fertilizante', methods=['POST'])
def registrar_fertilizante():
    datos = request.json
    sensor_id = datos.get('sensor_id')
    cantidad = datos.get('cantidad')
    timestamp = datos.get('timestamp')
    calcular_cantidad_fertilizante(sensor_id, cantidad, timestamp)
    return jsonify({'mensaje': 'Consumo de fertilizante registrado exitosamente'}), 201
