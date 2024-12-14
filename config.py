import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
