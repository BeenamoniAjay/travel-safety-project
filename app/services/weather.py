import requests


def fetch_weather(city, api_key):
    if not api_key:
        return {'temperature': 'N/A', 'description': 'Weather API key not configured'}

    url = (
        'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city},IN&appid={api_key}&units=metric'
    )

    try:
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        weather_data = response.json()
        temp = round(weather_data['main']['temp'], 1)
        desc = weather_data['weather'][0]['description']
        return {'temperature': temp, 'description': desc}
    except requests.RequestException:
        return {'temperature': 'N/A', 'description': 'Unable to fetch weather'}
