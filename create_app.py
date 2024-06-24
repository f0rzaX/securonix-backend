import os
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from auth import auth_bp
from data import data_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": os.getenv('FRONTEND_URL', 'http://localhost:5173')}})
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)

    return app
