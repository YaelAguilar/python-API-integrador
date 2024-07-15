from flask import Blueprint, jsonify

public_bp = Blueprint('public', __name__)

@public_bp.route('/public')
def public_route():
    return jsonify({'mensaje': 'Esta es una ruta pública'})
