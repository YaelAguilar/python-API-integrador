import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'jwt_secret_default')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_default')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret_default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://admin:themegapassword99@database-soursop.cwh2wgvynejc.us-east-1.rds.amazonaws.com/soursop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    