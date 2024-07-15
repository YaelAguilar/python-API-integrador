import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', None)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
