import os
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from auth import auth_bp
from data import data_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": app.config['FRONTEND_URL']}})

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(data_bp)

    return app
