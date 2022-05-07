from datetime import timedelta

from app import create_app

app = create_app()

@app.before_request
def before_request():
    app.permanent_session_lifetime = timedelta(minutes=10)
