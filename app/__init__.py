import os

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', None)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(12).hex())
    app.config['SESSION_TYPE'] = 'memcache'

    db.init_app(app)

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)

    login_configuration(app)
    register_blueprints(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_internal_server_error)

    return app

def login_configuration(app):
    from app.resources.user.models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect('/signin?next=' + request.path)

def register_blueprints(app):
    from app.resources.auth.views import auth_bp
    from app.resources.client.views import client_bp
    from app.resources.user.views import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
