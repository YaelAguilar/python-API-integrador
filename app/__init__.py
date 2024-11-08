import logging
import threading
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import pymysql

pymysql.install_as_MySQLdb()
from app.db import db
from app.config.config import Config
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
        from app.models.crecimiento_planta import CrecimientoPlanta
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