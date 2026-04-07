from app import create_app

app = create_app()   # ✅ this line is important

if __name__ == '__main__':
    app.run(debug=True)