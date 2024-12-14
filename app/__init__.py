from flask import Flask
from app.extensions import register_extensions
from app.models import *  # Importar todos os modelos para o contexto do app
from app.routes import register_routes  # Importa a função de registro de rotas

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.development.DevelopmentConfig")

    # Registra extensões (como SQLAlchemy e Migrate)
    register_extensions(app)

    # Registra as rotas do sistema
    register_routes(app)

    return app
