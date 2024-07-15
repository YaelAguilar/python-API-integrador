from flask import request, jsonify
from functools import wraps
import jwt
from app.models.user import User

def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Bearer <token>
        
        if not token:
            return jsonify({'mensaje': 'Token es requerido'}), 401
        
        try:
            datos = jwt.decode(token, request.app.config['SECRET_KEY'], algorithms=['HS256'])
            usuario_actual = User.query.filter_by(correo=datos['correo']).first()
        except Exception as e:
            return jsonify({'mensaje': 'Token es inválido', 'error': str(e)}), 401
        
        return f(usuario_actual, *args, **kwargs)
    
    return decorador
