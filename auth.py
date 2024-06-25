from datetime import timedelta
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db
from flask_jwt_extended import create_access_token
from flask import current_app as app
import requests

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signin", methods=["POST"])
def signin():
    email = request.json.get("email")
    password = request.json.get("password")
    user = User.query.filter_by(email=email).first()
    if user and user.password and check_password_hash(user.password, password):
        expires = timedelta(days=1)
        access_token = create_access_token(identity=email, expires_delta=expires)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid email or password"}), 401


@auth_bp.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email")
    password = request.json.get("password")
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201


# for Google OAuth
@auth_bp.route("/authorize", methods=["POST"])
def authorize():
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Missing token"}), 400

    # use the token to get user (from Google)
    try:
        resp = requests.get(
            app.config['GOOGLE_USER_INFO'],
            params={'alt': 'json'},
            headers={'Authorization': f'Bearer {token}'}
        )
        user_info = resp.json()
        email = user_info['email']
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
