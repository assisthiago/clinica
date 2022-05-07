from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required, login_user, logout_user
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
        flash('Usuário ou senha incorreta', 'danger')
        return redirect(url_for('auth.signin'))

    # if user.status == 'inativo':
    #     flash('Usuário indisponível', 'danger')
    #     return redirect(url_for('auth.signin'))

    login_user(user, remember=form['remember'])
    session['username'] = user.usuario

    flash(f'Olá, {user.usuario}', 'success')
    return redirect(url_for('auth.settings'))

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
        flash('Usuário cadastrado com sucesso', 'success')
        return redirect(url_for('auth.signin'))

    except:
        User.rollback(new_user)
        flash('Ocorreu um erro ao cadastrar o usuário', 'danger')
        return redirect(url_for('auth.signup'))

@auth_bp.route('/signout', methods=['GET'])
@login_required
def signout():
    logout_user()
    session.clear()

    return redirect(url_for('auth.signin'))

@auth_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'GET':
        units = [
            ('unit_1', 'Unidade 1'),
            ('unit_2', 'Unidade 2'),
            ('unit_3', 'Unidade 3')
        ]
        doctors = [
            ('doctor_1', 'José Maria'),
            ('doctor_2', 'Agostinho'),
            ('doctor_3', 'Bento')
        ]

        try:
            unit_id, doctor_id = None, None
            if 'doctor_unit' in session.keys():
                unit_id, doctor_id = session['doctor_unit']

            context = {
                'username': session['username'],
                'unit_id': unit_id, 'doctor_id': doctor_id,
                'units': units, 'doctors': doctors
            }
            return render_template('auth/settings.html', context=context)

        except:
            logout_user()
            session.clear()

            flash('Ocorreu um erro na configuração', 'danger')
            return redirect(url_for('auth.signin'))

    form = dict(request.form)

    """
    Dúvida:
    - Saber se essa relação de Auxiliar <> Unidade <> Médico será gravada no banco.
    """

    session['doctor_unit'] = form['unit_id'], form['doctor_id']
    return redirect(url_for('client.list'))
