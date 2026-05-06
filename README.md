# Travel Safety Web Application

A professional Flask web application for evaluating travel safety risks in Indian cities using machine learning and real-time weather data.

## Features

- **User Authentication**: Secure signup/login with password hashing
- **Risk Assessment**: ML-powered safety predictions for major Indian cities
- **Real-time Weather**: Live weather data integration
- **Dashboard**: User history and risk visualization with charts
- **Favorites**: Save and manage favorite destinations
- **Responsive Design**: Mobile-friendly Bootstrap UI
- **Search Suggestions**: Autocomplete city selection

## Tech Stack

- **Backend**: Flask 2.3+ with Blueprints
- **Database**: SQLAlchemy with SQLite
- **Security**: Flask-Bcrypt, Flask-WTF CSRF protection
- **Frontend**: Bootstrap 5, Chart.js, Custom CSS
- **ML**: Scikit-learn for risk prediction
- **APIs**: OpenWeatherMap for weather data

## Project Structure

```
travel-safety-project/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions
│   ├── models.py            # Database models
│   ├── auth/                # Authentication blueprint
│   │   ├── routes.py
│   │   └── forms.py
│   ├── main/                # Main app blueprint
│   │   └── routes.py
│   └── services/            # Business logic
│       ├── risk.py
│       └── weather.py
├── templates/               # Jinja2 templates
│   ├── layout.html
│   ├── dashboard.html
│   ├── result.html
│   ├── auth/
│   └── errors/
├── static/                  # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── data/                    # Dataset files
├── model/                   # ML model files
├── instance/                # Instance-specific config
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── app.py                   # Application entry point
├── wsgi.py                  # WSGI entry point
└── Procfile                 # Heroku deployment
```

## Setup Instructions

1. **Clone and Install Dependencies**:
   ```bash
   git clone <repository-url>
   cd travel-safety-project
   pip install -r requirements.txt
   ```

2. **Environment Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

3. **Initialize Database**:
   ```bash
   python app.py  # This will create the database automatically
   ```

4. **Run Development Server**:
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

## Configuration

### Required Environment Variables

- `SECRET_KEY`: Flask secret key for sessions
- `WEATHER_API_KEY`: OpenWeatherMap API key
- `DATABASE_URL`: Database connection string (default: SQLite)

### Optional Environment Variables

- `MODEL_PATH`: Path to ML model file
- `CITY_DATA_PATH`: Path to city dataset CSV

## API Endpoints

- `GET /`: Dashboard (requires login)
- `GET/POST /login`: User login
- `GET/POST /signup`: User registration
- `POST /logout`: User logout
- `POST /search`: Perform safety search
- `POST /favorite/<city>`: Add city to favorites

## Security Features

- Password hashing with bcrypt
- CSRF protection on forms
- SQL injection prevention with SQLAlchemy
- Secure session management
- Input validation and sanitization

## Deployment

### Heroku

1. Create Heroku app
2. Set environment variables in Heroku dashboard
3. Deploy using git push or Heroku CLI

### Local Production

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

## Development

### Running Tests

```bash
# Add tests in tests/ directory
pytest
```

### Code Quality

```bash
# Install development dependencies
pip install black flake8 mypy

# Format code
black .

# Lint code
flake8 .

# Type check
mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- City safety data from various public sources
- Weather data from OpenWeatherMap API
- UI components from Bootstrap
- Charts powered by Chart.js

<img width="1888" height="962" alt="image" src="https://github.com/user-attachments/assets/687a5041-7228-4766-9b72-aac153db6cd5" />
<img width="1900" height="1005" alt="image" src="https://github.com/user-attachments/assets/73f7cbda-19d4-454f-afe6-9815c102b472" />
<img width="1901" height="1004" alt="image" src="https://github.com/user-attachments/assets/408a795a-e9ab-40d3-ac4d-7352bc65ca4b" />
<img width="1886" height="1069" alt="image" src="https://github.com/user-attachments/assets/d77981eb-a18f-487a-94fe-32949ae8765a" />

