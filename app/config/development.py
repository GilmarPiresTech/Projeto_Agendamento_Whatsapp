class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"  # Banco SQLite para desenvolvimento
    SQLALCHEMY_TRACK_MODIFICATIONS = False

