from app.routes.main import main
from app.routes.appointments import appointments

def register_routes(app):
    app.register_blueprint(main)
    app.register_blueprint(appointments)
