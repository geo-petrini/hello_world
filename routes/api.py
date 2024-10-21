from flask import Blueprint, request, jsonify
# from flask import jsonify


api = Blueprint('api', __name__)

@api.route('/data', methods=['GET'])
def get_data():
    query_param = request.args.get('param')
    response = {
        'message': 'Received GET request',
        'param': query_param
    }
    # return jsonify(response), 200
    return response, 200

@api.route('/data', methods=['POST'])
def submit_data():
    # form_data = request.form.get('data')
    json_data = request.json.get('data')
    response = {
        'message': 'Received POST request',
        'data': json_data
    }
    return jsonify(response), 201

@api.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    updated_data = request.json
    response = {
        'message': 'Received PUT request',
        'id': id,
        'updated_data': updated_data
    }
    return jsonify(response), 200


@api.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    response = {
        'message': 'Received DELETE request',
        'id': id,
        'status': 'Resource deleted'
    }
    return jsonify(response), 200