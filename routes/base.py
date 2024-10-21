from flask import Blueprint
from flask import request, render_template

base = Blueprint('base', __name__)

@base.route('/')
def root():
    return "Hello, Flask!"

@base.route('/user/<username>')
def profile(username):
    return f'Profile page of {username}'

@base.route('/home/')
def home():
    return render_template('base/index.html')

@base.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        return "Form submitted!"
    else:
        return "Show the form."