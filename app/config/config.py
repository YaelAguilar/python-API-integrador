import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:ZjAnVZLSVqjKXHJjYwFiXbAuhlJNdfiY@roundhouse.proxy.rlwy.net:13499/railway')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT SECRET KEY ', 'jwt_secret default')