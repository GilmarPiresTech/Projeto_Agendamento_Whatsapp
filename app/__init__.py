from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Register extensions
    # Register blueprints
    
    return app
