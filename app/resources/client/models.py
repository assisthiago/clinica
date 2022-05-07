import pendulum
from sqlalchemy.orm import relationship
from sqlalchemy_imageattach.entity import Image, image_attachment

from app import db


class Client(db.Model):
    __tablename__ = 'Paciente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), unique=True)
    nascimento = db.Column(db.Date())
    telefone_1 = db.Column(db.Integer)
    telefone_2 = db.Column(db.Integer)
    matricula = db.Column(db.String(255))
    status = db.Column(db.String(100), default='ativo')
    cpf = db.Column(db.Integer)
    email = db.Column(db.String(100))
    foto = image_attachment('ClientPicture')
    histórico = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    criado_por = db.Column(db.String(100))
    atualizado_por = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime(), default=pendulum.now(tz='America/Sao_Paulo'))
    atualizado_em = db.Column(db.DateTime(), default=pendulum.now(tz='America/Sao_Paulo'), onupdate=pendulum.now(tz='America/Sao_Paulo'))

    def __init__(selfd) -> None:
        pass

    def __repr__(self) -> str:
        return f'Client {self.nome}'


class ClientPicture(Image):
    __tablename__ = 'PacienteFoto'
    client_id = db.Column(db.Integer, db.ForeignKey('Paciente.id'), primary_key=True)
    client = relationship('Client')
