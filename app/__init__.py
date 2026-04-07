from pathlib import Path
from flask import Flask, render_template
from sqlalchemy import inspect, text
from .config import Config
from .extensions import db, login_manager
from .auth.routes import auth_bp
from .main.routes import main_bp
from .services.risk import load_city_model

BASE_DIR = Path(__file__).resolve().parents[1]


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=str(BASE_DIR / 'templates'),
        static_folder=str(BASE_DIR / 'static'),
    )
    app.config.from_object(Config)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, server_error)

    with app.app_context():
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
        _migrate_user_email_column()
        db.create_all()
        load_city_model(app)

    return app


def _migrate_user_email_column():
    inspector = inspect(db.engine)
    if 'user' not in inspector.get_table_names():
        return

    columns = [col['name'] for col in inspector.get_columns('user')]
    if 'email' in columns:
        return

    with db.engine.connect() as conn:
        conn.execute(text('ALTER TABLE user ADD COLUMN email VARCHAR(120)'))
        conn.execute(text('UPDATE user SET email = username WHERE email IS NULL'))
        conn.execute(text('UPDATE user SET email = LOWER(email) WHERE email IS NOT NULL'))
        conn.commit()

def page_not_found(error):
    return render_template('errors/404.html'), 404


def server_error(error):
    return render_template('errors/500.html'), 500
