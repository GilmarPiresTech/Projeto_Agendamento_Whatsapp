from flask import Flask
from app.extensions import register_extensions
from app.models import *  # Importar todos os modelos para o contexto do app

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.development.DevelopmentConfig")

    # Registra extensões (como SQLAlchemy e Migrate)
    register_extensions(app)

    return app
