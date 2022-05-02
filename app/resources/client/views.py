from flask import Blueprint, render_template
from flask_login import login_required

client_bp = Blueprint('client', __name__)

@client_bp.route('/', methods=['GET'])
@login_required
def get_clients():
    return render_template('index.html')
