from flask import Flask, url_for, request, render_template
from flask import jsonify
from routes.base import base
from routes.admin import admin
from routes.api import api

app = Flask(__name__)

app.register_blueprint(base)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(admin, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)