from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    pass

@auth_bp.route("/signin", methods=["GET", "POST"])
def login():
    pass

