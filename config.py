import os
import cryptography
print("cryptography installed successfully")

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_default_fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Andre4301$$@localhost/birdyphillips'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join('static', 'uploads')