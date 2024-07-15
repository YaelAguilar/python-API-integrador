from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from app.config.config import Config
from app.db import db
from threading import Thread
from app.utils.rabbitmq_subscriber import start_consuming

load_dotenv()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # Importar todos los modelos aquí
        from app.models.user import User
        from app.models.sensor import Sensor
        from app.models.lectura_sensor import LecturaSensor
        from app.models.consumo_agua import ConsumoAgua
        from app.models.consumo_fertilizante import ConsumoFertilizante
        from app.models.estado_planta import EstadoPlanta
        from app.models.estimativo_produccion import EstimativoProduccion

        db.create_all()

        from app.routes.auth_routes import auth_bp
        from app.routes.public_routes import public_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(public_bp)

    # Iniciar el suscriptor de RabbitMQ en un hilo separado
    Thread(target=start_consuming).start()

    return app
