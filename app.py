import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRECT_KEY'] = os.urandom(12).hex()

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    # login_config(app)
    register_blueprints(app)

    return app

def login_config(app):
    # from auxiliar.models import Auxiliar

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(auxiliar_id):
    #     return Auxiliar.query.get(int(auxiliar_id))

def register_blueprints(app):
    from resources.auth.views import auth_bp

    app.register_blueprint(auth_bp)
