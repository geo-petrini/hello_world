import os
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
# from flask import Blueprint

from models.conn import db
from models.model import *

from flask_migrate import Migrate

from flask_login import LoginManager
from flask_login import login_required


from routes.api import api as bp_api
from routes.auth import auth as bp_auth


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp_api,  url_prefix='/api')    
app.register_blueprint(bp_auth,  url_prefix='/auth')    

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_hello_adm:miapassword1@localhost/flask_hello'
app.config['SECRET_KEY'] = 'kjfsdkjskdfjk keksj lf123 s'
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#L'opzione SQLALCHEMY_TRACK_MODIFICATIONS è una configurazione per Flask-SQLAlchemy che determina se SQLAlchemy deve o meno tenere traccia delle modifiche sugli oggetti per ogni sessione.
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    init_db()

# flask_login user loader block
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    # return User.query.get(int(user_id))
    return user


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hello/<username>')
def hello(username):
    return render_template('hello.html', username=username)

@app.route('/power/<int:value>')
def power(value):
    return f'value: {value*value}'

@app.route('/sum/', methods=['POST'])
def sum():
    values = request.json
    v1 = values["v1"]
    v2 = values["v2"]
    return f'{v1+v2}'


@app.route('/dashboard')
@login_required
@user_has_role('admin') # oppure @user_has_role('admin', 'moderator')
def admin_dashboard():
    return 'dashboard'
    # return render_template('admin_dashboard.html')



# OLD user functions
# @app.route('/createuser', methods=['POST'])
# def create_user():
#     values = request.json
#     username = values["username"]
#     email = values["email"]    
#     password = values["password"]    
#     # username = request.vars['username'] #in caso di form possiamo usare request.form
#     # email = request.vars['email']
#     # password = request.vars['password']
#     user = User(username=username, email=email)
#     user.set_password(password)  # Imposta la password criptata
#     db.session.add(user)  # equivalente a INSERT
#     db.session.commit()
#     return f"Utente {username} creato con successo."

# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     # return render_template("user/detail.html", user=user)
#     return f'{user}'


# @app.route("/user/<int:id>", methods=['POST', 'PUT'])
# def user_update(id):
#     user = db.get_or_404(User, id)
#     values = request.json
#     username = values["username"] if 'username' in values else None
#     email = values["email"]     if 'email' in values else None
#     password = values["password"] if 'password' in values else None
#     if request.method == "POST":
#         user.username = username
#         user.email = email
#         user.set_password(password)
#         db.session.commit()

#     if request.method == "PUT":
#         if username and user.username != username: user.username = username 
#         if email and user.email != email: user.email = email
#         if password and not user.check_password(password): user.set_password(password)
#         db.session.commit()

#     return f'{user}'

if __name__ == '__main__':
    app.run(debug=True)
