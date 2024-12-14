class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://agendadorwhats:Gp20262595!@186.202.152.237/agendadorwhats"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,  # Recicla conexões após 280 segundos
        "pool_size": 10,      # Número de conexões no pool
        "max_overflow": 5,    # Número máximo de conexões extras
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False