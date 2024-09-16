from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

exa = Blueprint('examples', __name__)

@exa.route('/hello/<username>')
def hello(username):
    return render_template('hello.html', username=username)

@exa.route('/power/<int:value>')
def power(value):
    return f'value: {value*value}'

@exa.route('/sum/', methods=['POST'])
def sum():
    values = request.json
    v1 = values["v1"]
    v2 = values["v2"]
    return f'{v1+v2}'


# OLD user functions
@exa.route('/createuser', methods=['POST'])
def create_user():
    values = request.json
    username = values["username"]
    email = values["email"]    
    password = values["password"]    
    # username = request.vars['username'] #in caso di form possiamo usare request.form
    # email = request.vars['email']
    # password = request.vars['password']
    user = User(username=username, email=email)
    user.set_password(password)  # Imposta la password criptata
    db.session.add(user)  # equivalente a INSERT
    db.session.commit()
    return f"Utente {username} creato con successo."

@exa.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    # return render_template("user/detail.html", user=user)
    return f'{user}'


@exa.route("/user/<int:id>", methods=['POST', 'PUT'])
def user_update(id):
    user = db.get_or_404(User, id)
    values = request.json
    username = values["username"] if 'username' in values else None
    email = values["email"]     if 'email' in values else None
    password = values["password"] if 'password' in values else None
    if request.method == "POST":
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.commit()

    if request.method == "PUT":
        if username and user.username != username: user.username = username 
        if email and user.email != email: user.email = email
        if password and not user.check_password(password): user.set_password(password)
        db.session.commit()

    return f'{user}'