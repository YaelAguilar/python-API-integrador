import logging
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from app.config.config import Config
from app.db import db
from threading import Thread
from app.utils.rabbitmq_subscriber import start_consuming
from app.utils.websocket_client import connect_to_server, disconnect_from_server

load_dotenv()

jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)  # CORS

    with app.app_context():
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
        from app.routes.sensor_routes import sensor_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(public_bp)
        app.register_blueprint(sensor_bp, url_prefix='/sensor')

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app

def run_rabbitmq_subscriber(app):
    with app.app_context():
        app.logger.info("Iniciando el suscriptor de RabbitMQ")
        start_consuming()

def run_websocket_client():
    print("Iniciando el cliente WebSocket")
    connect_to_server()
    print("Cliente WebSocket iniciado")

if __name__ == '__main__':
    print("Ejecutando la aplicación")
    app = create_app()

    thread_rabbitmq = Thread(target=run_rabbitmq_subscriber, args=(app,))
    thread_rabbitmq.start()

    thread_websocket = Thread(target=run_websocket_client)
    thread_websocket.start()

    app.run(host='0.0.0.0', port=3004)

    thread_rabbitmq.join()
    thread_websocket.join()
