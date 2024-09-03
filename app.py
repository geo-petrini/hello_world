from flask import Flask
from flask import render_template
from flask import request
# from flask import Blueprint
from routes.api import api as bp_api

app = Flask(__name__)
app.register_blueprint(bp_api,  url_prefix='/api')    

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