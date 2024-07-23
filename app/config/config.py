import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret default')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://admin:themegapassword99@database-soursop.cwh2wgvynejc.us-east-1.rds.amazonaws.com/soursop')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
<<<<<<< HEAD
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret default')
=======
>>>>>>> 457cb10720d9d51a8d44033ffff930adb5f3de7d
