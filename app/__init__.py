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

load_dotenv()

jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app) #CORS

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
