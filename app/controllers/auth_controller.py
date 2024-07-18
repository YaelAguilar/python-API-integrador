from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import re
from app.models.user import User
from app.db import db

def register():
    datos = request.json
    nombre = datos.get('nombre')
    apellidos = datos.get('apellidos')
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    if not nombre or not apellidos or not correo or not contraseña:
        return jsonify({'mensaje': 'Datos faltantes'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
        return jsonify({'mensaje': 'Formato de correo inválido'}), 400
    if len(contraseña) < 8:
        return jsonify({'mensaje': 'La contraseña debe tener al menos 8 caracteres'}), 400

    usuario_existente = User.query.filter_by(correo=correo).first()
    if usuario_existente:
        return jsonify({'mensaje': 'El usuario ya existe'}), 400

    contraseña_hash = generate_password_hash(contraseña)
    nuevo_usuario = User(nombre=nombre, apellidos=apellidos, correo=correo, contraseña_hash=contraseña_hash)
    db.session.add(nuevo_usuario)
    db.session.commit()

    access_token = create_access_token(identity={'correo': correo}, expires_delta=datetime.timedelta(days=7))

    return jsonify({'mensaje': 'Usuario registrado exitosamente', 'token': access_token}), 201

def login():
    datos = request.json
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    if not correo or not contraseña:
        return jsonify({'mensaje': 'Datos faltantes'}), 400

    usuario = User.query.filter_by(correo=correo).first()

    if usuario and check_password_hash(usuario.contraseña_hash, contraseña):
        access_token = create_access_token(identity={'correo': usuario.correo}, expires_delta=datetime.timedelta(days=7))
        return jsonify({'token': access_token, 'usuario': {
            'id': usuario.id,
            'email': usuario.correo,
            'nombre': usuario.nombre,
            'apellidos': usuario.apellidos
        }}), 200
    else:
        return jsonify({'mensaje': 'Credenciales inválidas'}), 401

@jwt_required()
def protected_route():
    usuario_actual = get_jwt_identity()
    return jsonify({'mensaje': 'Esta es una ruta protegida', 'usuario': usuario_actual})
