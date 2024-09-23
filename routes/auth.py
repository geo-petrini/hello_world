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

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    # return 'Login'
    return render_template('auth/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # user = User.query.filter_by(email=email).first()
    stmt = db.select(User).filter_by(email=email)
    user = db.session.execute(stmt).scalar_one_or_none()    

    current_app.logger.info(f'user: {user}')
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.check_password(password):
        current_app.logger.error(f'user {email} not logged with password: {password}')
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('auth.profile'))    

@auth.route('/signup', methods=['GET'])
def signup():
    # return 'Signup' template
    return render_template('auth/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # signup input validation and logic
    #TODO verify password strenght
    # username = request.form["username"] #as an alternative use request.form.get("username")
    # email = request.form["email"]    
    # password = request.form["password"]
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')    

    if not username:
        flash('Invalid username')
        return redirect(url_for('auth.signup'))
    if not email:
        flash('Invalid email')
        return redirect(url_for('auth.signup'))
    if not password:
        flash('Invalid password')
        return redirect(url_for('auth.signup'))                
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        # display some kind of error
        flash('User with this email address already exists')
        return redirect(url_for('auth.signup'))

    user = User(username=username, email=email)
    user.set_password(password)  # Imposta la password criptata
    db.session.add(user)  # equivalente a INSERT
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', name=current_user.username)