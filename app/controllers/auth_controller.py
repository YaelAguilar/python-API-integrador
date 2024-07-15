from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import re
from app.models.user import User
from app import db
from app.utils.token import token_requerido

def register():
    datos = request.json
    nombre = datos.get('nombre')
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    if not correo or not contraseña:
        return jsonify({'mensaje': 'Datos faltantes'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        return jsonify({'mensaje': 'Formato de correo inválido'}), 400
    if len(contraseña) < 8:
        return jsonify({'mensaje': 'La contraseña debe tener al menos 8 caracteres'}), 400

    usuario_existente = User.query.filter_by(correo=correo).first()
    if usuario_existente:
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    contraseña_hash = generate_password_hash(contraseña)
    nuevo_usuario = User(nombre=nombre, correo=correo, contraseña_hash=contraseña_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()

    payload = {
        'correo': correo,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, request.app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'mensaje': 'Usuario registrado exitosamente', 'token': token}), 201

def login():
    datos = request.json
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    usuario = User.query.filter_by(correo=correo).first()

    if usuario and check_password_hash(usuario.contraseña_hash, contraseña):
        payload = {
            'correo': correo,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        token = jwt.encode(payload, request.app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'mensaje': 'Inicio de sesión exitoso', 'token': token}), 200
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401

@token_requerido
def protected_route(usuario_actual):
    return jsonify({'mensaje': 'Esta es una ruta protegida', 'usuario': usuario_actual.nombre})
