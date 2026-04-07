import pickle
import pandas as pd
from pathlib import Path
from math import floor


def load_city_model(app):
    city_data = pd.read_csv(app.config['CITY_DATA_PATH'])
    app.city_data = city_data
    app.city_list = sorted(city_data['city'].dropna().astype(str).tolist())
    app.risk_model = None


def _ensure_risk_model(app):
    if getattr(app, 'risk_model', None) is not None:
        return

    model_path = Path(app.config['MODEL_PATH'])
    if not model_path.exists():
        raise RuntimeError(f'Model file not found at {model_path}')

    with model_path.open('rb') as handle:
        app.risk_model = pickle.load(handle)


def predict_risk(city, app):
    city = city.strip()
    data = app.city_data
    row = data[data['city'].str.lower() == city.lower()]
    if row.empty:
        return {
            'label': 'Unknown',
            'score': 0,
            'description': 'City not found in dataset.',
            'color': 'secondary',
        }

    _ensure_risk_model(app)

    row = row.iloc[0]
    input_df = pd.DataFrame(
        [[row['crime'], row['disaster'], row['health']]],
        columns=['crime', 'disaster', 'health'],
    )
    label = app.risk_model.predict(input_df)[0]

    score_map = {'High': 90, 'Medium': 55, 'Low': 25}
    colors = {'High': 'danger', 'Medium': 'warning', 'Low': 'success'}
    descriptions = {
        'High': 'High risk area. Travel with strong caution.',
        'Medium': 'Moderate risk. Stay alert and plan carefully.',
        'Low': 'Low risk. A good destination with standard precautions.',
    }

    score = score_map.get(label, 0)
    return {
        'label': label,
        'score': score,
        'description': descriptions.get(label, 'Risk assessment unavailable.'),
        'color': colors.get(label, 'secondary'),
        'image': f'images/{row.city}.jpg',
    }
