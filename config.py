import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'sentiment.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads' 