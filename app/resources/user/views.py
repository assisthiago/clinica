from flask import render_template, request, Blueprint
from flask_login import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/account', methods=['GET'])
@login_required
def account():
    return render_template('user/account.html')
