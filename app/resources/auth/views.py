from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.resources.user.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET'])
def signin():
    return render_template('auth/signin.html')

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
