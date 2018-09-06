#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


proteins = [
    {
        'name': u'Albumin',
        'id': u'ALBU_HUMAN',
        'function': u'Regulates colloidal osmotic pressure of blood'
    },
    {
        'name': u'Immunoglobulin heavy constant gamma 1',
        'id': u'IGHG1_HUMAN',
        'function': u'Antigen binding'
    },
    {
        'name': u'Transferrin',
        'id': u'TRFE_HUMAN',
        'function': u'Iron binding and transport'
    }
]

# GET


@app.route('/multiprot/<string:id>', methods=['GET'])
def get_protein(id):
    result = [item for item in proteins if item['id'] == id]
    return jsonify(result)


@app.route('/multiprot/<string:id>/name', methods=['GET'])
def get_protein_name(id):
    result = [item['name'] for item in proteins if item['id'] == id]
    return result[0]


@app.route('/multiprot/<string:id>/function', methods=['GET'])
def get_protein_function(id):
    result = [item['function'] for item in proteins if item['id'] == id]
    return result[0]

# POST


@auth.login_required
@app.route('/multiprot/add/', methods=['POST'])
def add_protein():
    if 'id' in request.json and 'name' in request.json and 'function' in request.json:
        protein = {'id': request.json['id'], 'name': request.json['name'], 'function': request.json['function']}
        proteins.append(protein)
    else:
        abort(400)
    return jsonify({'proteins': proteins})

# PUT


@auth.login_required
@app.route('/multiprot/<string:id>/edit/', methods=['PUT'])
def edit_protein(id):
    protein = [item for item in proteins if item['id'] == id]
    if len(protein) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json:
        protein[0]['name'] = request.json['name']
    if 'function' in request.json:
        protein[0]['function'] = request.json['function']
    return jsonify(protein)

# DELETE


@auth.login_required
@app.route('/multiprot/<string:id>/delete', methods=['DELETE'])
def delete_protein(id):
    protein = [item for item in proteins if item['id'] == id]
    if len(protein) == 0:
        abort(404)
    proteins.remove(protein[0])
    return 'Protein deleted'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)