import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    PORT = int(os.getenv('PORT'))
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    FRONTEND_URL = os.getenv('FRONTEND_URL')
    ROWS_PER_PAGE = int(os.getenv('ROWS_PER_PAGE', 25))

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_USER_INFO = os.getenv('GOOGLE_USER_INFO', "https://www.googleapis.com/oauth2/v1/userinfo")