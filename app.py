from flask import Flask
from flask import render_template
from flask import request
# from flask import Blueprint

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from routes.api import api as bp_api

app = Flask(__name__)
app.register_blueprint(bp_api,  url_prefix='/api')    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#L'opzione SQLALCHEMY_TRACK_MODIFICATIONS è una configurazione per Flask-SQLAlchemy che determina se SQLAlchemy deve o meno tenere traccia delle modifiche sugli oggetti per ogni sessione.


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importa i modelli
from models import User


@app.route('/')
def home():
    return "Hello, Flask!"

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


if __name__ == '__main__':
    app.run(debug=True)