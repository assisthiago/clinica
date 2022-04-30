from crypt import methods
from flask import Blueprint, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signin', methods=['GET'])
def get_signin():
    return render_template('auth/signin.html')

@auth_bp.route('/signup', methods=['GET'])
def get_signup():
    return render_template('auth/signup.html')
