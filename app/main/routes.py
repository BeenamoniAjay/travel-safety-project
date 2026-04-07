from collections import Counter
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..extensions import db
from ..models import FavoriteLocation, SearchHistory
from ..services.weather import fetch_weather
from ..services.risk import predict_risk

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    history = (
        SearchHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(SearchHistory.created_at.desc())
        .limit(10)
        .all()
    )
    favorites = (
        FavoriteLocation.query
        .filter_by(user_id=current_user.id)
        .order_by(FavoriteLocation.added_at.desc())
        .all()
    )

    risk_counts = Counter(item.risk_label for item in history)
    chart_data = {
        'labels': ['Low', 'Medium', 'High'],
        'values': [risk_counts.get('Low', 0), risk_counts.get('Medium', 0), risk_counts.get('High', 0)],
    }

    return render_template(
        'dashboard.html',
        city_list=current_app.city_list,
        history=history,
        favorites=favorites,
        chart_data=chart_data,
    )


def find_city(city, city_list):
    normalized = city.strip().lower()
    for item in city_list:
        if item.lower() == normalized:
            return item
    return None


@main_bp.route('/search', methods=['POST'])
@login_required
def search():
    raw_city = request.form.get('city', '').strip()
    if not raw_city:
        flash('Please select a city before searching.', 'warning')
        return redirect(url_for('main.dashboard'))

    city = find_city(raw_city, current_app.city_list)
    if not city:
        flash('That city is not available. Please choose from the suggestions.', 'danger')
        return redirect(url_for('main.dashboard'))

    risk = predict_risk(city, current_app)
    weather = fetch_weather(city, current_app.config['WEATHER_API_KEY'])
    existing_favorite = FavoriteLocation.query.filter_by(user_id=current_user.id, city=city).first()

    search_history = SearchHistory(
        user_id=current_user.id,
        city=city,
        risk_label=risk['label'],
        score=risk['score'],
        weather=weather['description'],
    )
    db.session.add(search_history)
    db.session.commit()

    return render_template(
        'result.html',
        city=city,
        risk=risk,
        weather=weather,
        is_favorite=bool(existing_favorite),
    )


@main_bp.route('/favorite/<city>', methods=['POST'])
@login_required
def add_favorite(city):
    city_match = find_city(city, current_app.city_list)
    if not city_match:
        flash('Unable to add that city as a favorite.', 'danger')
        return redirect(url_for('main.dashboard'))

    existing = FavoriteLocation.query.filter_by(user_id=current_user.id, city=city_match).first()
    if existing:
        flash(f'{city_match} is already in your favorites.', 'info')
        return redirect(url_for('main.dashboard'))

    favorite = FavoriteLocation(user_id=current_user.id, city=city_match)
    db.session.add(favorite)
    db.session.commit()
    flash(f'{city_match} has been added to favorites.', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route('/favorite/remove/<int:favorite_id>', methods=['POST'])
@login_required
def remove_favorite(favorite_id):
    favorite = FavoriteLocation.query.get_or_404(favorite_id)
    if favorite.user_id != current_user.id:
        flash('You are not authorized to remove that favorite.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(favorite)
    db.session.commit()
    flash(f'{favorite.city} was removed from favorites.', 'success')
    return redirect(url_for('main.dashboard'))
