from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy
db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)
