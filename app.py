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
from routes.admin import admin as bp_admin
from routes.examples import exa as bp_exa


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp_api,  url_prefix='/api')    
app.register_blueprint(bp_auth,  url_prefix='/auth')    
app.register_blueprint(bp_admin,  url_prefix='/admin')    
app.register_blueprint(bp_exa,  url_prefix='/examples')    

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



if __name__ == '__main__':
    app.run(debug=True)
