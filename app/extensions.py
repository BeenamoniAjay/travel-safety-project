from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

# Note: Using werkzeug.security instead of flask-bcrypt for simplicity
from werkzeug.security import generate_password_hash, check_password_hash

class Bcrypt:
    @staticmethod
    def generate_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def check_password_hash(hash, password):
        return check_password_hash(hash, password)

bcrypt = Bcrypt()
