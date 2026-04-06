from flask import Flask, render_template, request, redirect, session
import sqlite3
import pickle
import pandas as pd
import requests

app = Flask(__name__)
app.secret_key = "secret123"

# Load model
model = pickle.load(open("model/model.pkl", "rb"))
data = pd.read_csv("data/data.csv")

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template("index.html")

# -------- SIGNUP --------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # Check if user exists
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            error = "User already exists"
        else:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')

        conn.close()

    return render_template("signup.html", error=error)

# -------- LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# -------- RESULT --------
@app.route('/result', methods=['POST'])
def result():
    if 'user' not in session:
        return redirect('/login')

    city = request.form['city']

    row = data[data['city'] == city].iloc[0]

    crime = row['crime']
    disaster = row['disaster']
    health = row['health']

    input_data = pd.DataFrame([[crime, disaster, health]],
                              columns=['crime','disaster','health'])

    prediction = model.predict(input_data)[0]

    image = f"images/{city}.jpg"

    if prediction == "High":
        desc = "High risk area. Travel with caution."
        color = "red"
    elif prediction == "Medium":
        desc = "Moderate risk. Stay alert."
        color = "orange"
    else:
        desc = "Safe place. Enjoy your trip!"
        color = "green"

    # WEATHER
    api_key = "577cd8fe290f2527206580a2b5590ad6"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"

    response = requests.get(url)
    weather_data = response.json()

    if weather_data["cod"] == 200:
        temp = round(weather_data["main"]["temp"], 1)
        weather_desc = weather_data["weather"][0]["description"]
    else:
        temp = "N/A"
        weather_desc = "No data"

    return render_template("result.html",
                           danger=prediction,
                           city=city,
                           image=image,
                           desc=desc,
                           color=color,
                           temp=temp,
                           weather_desc=weather_desc)

if __name__ == '__main__':
    app.run(debug=True)