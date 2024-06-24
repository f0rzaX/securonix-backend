# config.py
import os

class Config:
    PORT = int(os.getenv('PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:pass@localhost/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'g00d_key_for_token_generation')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    ROWS_PER_PAGE = int(os.getenv('ROWS_PER_PAGE', 25))

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')