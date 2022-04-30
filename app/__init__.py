import os

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'), 404

def page_internal_server_error(e):
    return render_template('500.html'), 404

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRECT_KEY'] = os.urandom(12).hex()

    db.init_app(app)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_internal_server_error)

    return app

