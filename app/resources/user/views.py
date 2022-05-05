from flask import redirect, render_template, request, Blueprint, session, url_for, flash
from flask_login import login_required

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

    if User.get_by_username(form['username']):
        flash('Usuário já existente', 'danger')
        return render_template('user/account.html', context=context)


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
    user.nome = form['name']
    user.sobrenome = form['last_name']
    user.cargo = form['responsability']
    user.crm = form['crm']

    try:
        User.update()
        flash('Usuário atualizado com sucesso', 'success')

    except:
        User.rollback()
        flash('Ocorreu um erro ao atualizar o usuário', 'danger')

    finally:
        return redirect(url_for('user.account'))
