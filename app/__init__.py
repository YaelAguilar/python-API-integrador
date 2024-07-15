from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from app.config.config import Config
from app.db import db  # Importa db desde el archivo db.py

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Importar aquí para evitar importaciones circulares
        from app.models.user import User
        db.create_all()

        from app.routes.auth_routes import auth_bp
        from app.routes.public_routes import public_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(public_bp)

    return app
