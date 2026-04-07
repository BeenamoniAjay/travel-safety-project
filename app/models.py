from datetime import datetime
from .extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    searches = db.relationship('SearchHistory', backref='user', lazy=True)
    favorites = db.relationship('FavoriteLocation', backref='user', lazy=True)

    @property
    def username(self):
        return self.email

    def __repr__(self):
        return f'<User {self.email}>'


class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    risk_label = db.Column(db.String(32), nullable=False)
    score = db.Column(db.Float, nullable=False)
    weather = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SearchHistory {self.city} {self.risk_label}>'


class FavoriteLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FavoriteLocation {self.city}>'
