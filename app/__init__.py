from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        # Create all tables
        db.create_all()
    
    return app 