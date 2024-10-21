from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/')
def root():
    return render_template('admin/index.html')

@admin.route('/dashboard')
def dashboard():
    return "Admin Dashboard"
