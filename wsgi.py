from app import app

app.db.init_app(app=app.create_app())
