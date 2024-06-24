import os

import numpy as np
import pandas as pd

from flask import Flask
from flask_cors import CORS
from config import Config

from extensions import db, jwt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from auth import auth_bp
from data import data_bp


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv('FRONTEND_URL', 'http://localhost:5173')}})
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(
        db.String(255)
    )

app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 5000))