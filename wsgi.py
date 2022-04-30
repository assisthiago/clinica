from . import app
app.db.create_all(app=app.create_app)
