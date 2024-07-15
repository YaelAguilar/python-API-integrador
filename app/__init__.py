from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from app.config.config import Config
from app.db import db
from app.models.user import User
from app.models.Sensor import Sensor
from app.models.LecturaSensor import LecturaSensor
from app.models.ConsumoAgua import ConsumoAgua
from app.models.ConsumoFertilizante import ConsumoFertilizante
from app.models.EstadoPlanta import EstadoPlanta
from app.models.EstimativoProduccion import EstimativoProduccion


load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.models import (
            User,
            Sensor,
            LecturaSensor,
            ConsumoAgua,
            ConsumoFertilizante,
            EstadoPlanta,
            EstimativoProduccion
        )
        db.create_all()

        from app.routes.auth_routes import auth_bp
        from app.routes.public_routes import public_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(public_bp)

    return app
