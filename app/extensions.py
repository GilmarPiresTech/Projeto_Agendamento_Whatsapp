from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def register_extensions(app):
    db.init_app(app)      # Configura o SQLAlchemy
    migrate.init_app(app, db)  # Configura o Flask-Migrate
