from flask import Blueprint
from flask import jsonify
from colorhash import ColorHash

api = Blueprint('api', __name__)

@api.route('/dashboard')
def dashboard():
    return "API Dashboard"

@api.route('/<input>')
def generate(input):
    out = []
    for char in input:
        c = ColorHash(char)
        out.append(c.hex)
    return jsonify(out)
