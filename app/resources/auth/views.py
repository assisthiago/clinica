from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

from app.resources.user.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('auth/signin.html')

    form = dict(request.form)
    user = User.get_by_username(form['username'])

    if not user or not check_password_hash(user.senha, form['password']):
        flash('Usuário ou senha incorreta.', 'danger')
        return redirect(url_for('auth.signin'))

    login_user(user, remember=form['remember'])
    return redirect(url_for('client.list'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    form = dict(request.form)
    if User.get_by_username(form['username']):
        flash('Usuário já cadastrado', 'danger')
        return redirect(url_for('auth.signup'))

    new_user = User(**form)
    try:
        User.add(new_user)
        flash('Usuário cadastrado com sucesso.', 'success')
        return redirect(url_for('auth.signin'))

    except:
        User.rollback(new_user)
        flash('Ocorreu um erro ao cadastrar o usuário.', 'danger')
        return redirect(url_for('auth.signup'))
