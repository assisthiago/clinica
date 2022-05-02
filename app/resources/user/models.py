from email.policy import default
import pendulum
from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'Auxiliar'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    status = db.Column(db.String(100), default='ativo')
    criado_em = db.Column(db.DateTime(), default=pendulum.now(tz='America/Sao_Paulo'))
    atualizado_em = db.Column(db.DateTime(), default=pendulum.now(tz='America/Sao_Paulo'))

    def __init__(self, username, password) -> None:
        self.usuario = username
        self.senha = password

    def __repr__(self) -> str:
        return f'User {self.usuario}'

    @staticmethod
    def add(user):
        db.session.add(user)
        db.session.commit()
        db.session.close()

    def rollback(user):
        db.session.rollback()
        db.session.close()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(usuario=username).first() or None
