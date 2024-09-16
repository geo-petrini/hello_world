from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from flask_login import login_user, logout_user, login_required, current_user

from models.conn import db
from models.model import *

admin = Blueprint('admin', __name__)

@admin.route('/')
def default():
    return 'admin default'

@admin.route('/dashboard')
@login_required
@user_has_role('admin') # oppure @user_has_role('admin', 'moderator')
def default():
    #oppure if not current_user.has_role('admin'): return redirect(url_for('login'))
    return 'admin default'