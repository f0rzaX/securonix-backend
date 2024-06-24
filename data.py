from flask import Blueprint
from flask_jwt_extended import jwt_required

data_bp = Blueprint('data', __name__)
