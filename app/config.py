import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
INSTANCE_DIR = BASE_DIR / 'instance'

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
    load_dotenv(INSTANCE_DIR / '.env')
except ImportError:
    pass  # dotenv not installed, use environment variables directly


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f'sqlite:///{INSTANCE_DIR / "app.db"}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    MODEL_PATH = os.getenv('MODEL_PATH', str(BASE_DIR / 'model' / 'model.pkl'))
    CITY_DATA_PATH = os.getenv('CITY_DATA_PATH', str(BASE_DIR / 'data' / 'data.csv'))
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    JSON_SORT_KEYS = False
