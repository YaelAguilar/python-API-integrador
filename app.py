import ssl
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import logging
import os
from threading import Thread
import pymysql
pymysql.install_as_MySQLdb()

from app.config.config import Config
from app.db import db
from app.config.rabbitmq import start_consuming

load_dotenv()

jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

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
    from app.utils.websocket_client import connect_to_server, start_listening_to_rabbitmq
    connect_to_server()
    start_listening_to_rabbitmq()

if __name__ == '__main__':
    app = create_app()
    print("Ejecutando la aplicación")

    if not hasattr(app, 'thread_rabbitmq'):
        print("Iniciando el hilo del suscriptor de RabbitMQ")
        app.thread_rabbitmq = Thread(target=run_rabbitmq_subscriber, args=(app,))
        app.thread_rabbitmq.start()

    if not hasattr(app, 'thread_websocket'):
        print("Iniciando el cliente WebSocket")
        app.thread_websocket = Thread(target=run_websocket_client)
        app.thread_websocket.start()

    '''
    certfile_path = os.getenv('CERTFILE_PATH')
    keyfile_path = os.getenv('KEYFILE_PATH')
    
    if certfile_path and keyfile_path:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.load_cert_chain(certfile=certfile_path, keyfile=keyfile_path)
        app.run(ssl_context=context, host='0.0.0.0', port=3004, debug=True)
    else:
    '''
    app.run(host='0.0.0.0', port=3004, debug=True)

    app.thread_rabbitmq.join()
    app.thread_websocket.join()
