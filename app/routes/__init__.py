from app.routes.main import main

def register_routes(app):
    app.register_blueprint(main)
