from flask import Flask
from app.extensions import register_extensions
from app.routes import register_routes

def create_app():
    # Inicializa o app Flask
    app = Flask(__name__)

    # Configurações básicas
    app.config.from_object("app.config.development.DevelopmentConfig")

    # Registra extensões (SQLAlchemy, por exemplo)
    register_extensions(app)

    # Registra rotas
    register_routes(app)

    return app
