from flask import redirect, render_template, request, Blueprint, session, url_for, flash
from flask_login import login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.resources.user.models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.get_by_username(session['username'])
    context = {'user': user}

    if request.method == 'GET':
        return render_template('user/account.html', context=context)

    form = dict(request.form)
    user.usuario = form['username']
    user.status = 'ativo' if 'status' in form.keys() else 'inativo'

    try:
        User.update()
        flash('Usuário atualizado com sucesso', 'success')

    except:
        User.rollback()
        flash('Ocorreu um erro ao atualizar o usuário', 'danger')

    finally:
        user = User.get_by_username(form['username'])
        session['username'] = user.usuario
        context['user'] = user
        return render_template('user/account.html', context=context)

@user_bp.route('/info', methods=['POST'])
@login_required
def info():
    user = User.get_by_username(session['username'])

    form = dict(request.form)
    user.nome = form['first_name'] or None
    user.sobrenome = form['last_name'] or None
    user.cargo = form['responsibility'] or None
    user.crm = form['crm'] or None

    try:
        User.update()
        flash('Usuário atualizado com sucesso', 'success')

    except:
        User.rollback()
        flash('Ocorreu um erro ao atualizar o usuário', 'danger')

    finally:
        return redirect(url_for('user.account'))

@user_bp.route('/password', methods=['POST'])
@login_required
def change_password():
    user = User.get_by_username(session['username'])

    form = dict(request.form)
    if not check_password_hash(user.senha, form['password']):
        flash('Senha incorreta', 'danger')
    else:
        try:
            new_password = generate_password_hash(form['new_password'], method='sha256')
            user.senha = new_password
            User.update()
            flash('Senha atualizada com sucesso', 'success')
        except:
            User.rollback()
            flash('Ocorreu um erro ao atualizar a senha', 'danger')

        finally:
            return redirect(url_for('user.account'))
