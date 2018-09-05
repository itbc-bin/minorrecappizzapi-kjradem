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
        'id': 1,
        'name': u'Albumin',
        'code': u'ALBU_HUMAN',
        'function': u'Regulates colloidal osmotic pressure of blood'
    },
    {
        'id': 2,
        'name': u'Immunoglobulin heavy constant gamma 1',
        'code': u'IGHG1_HUMAN',
        'function': u'Antigen binding'
    },
    {
        'id': 3,
        'name': u'Transferrin',
        'code': u'TRFE_HUMAN',
        'function': u'Iron binding and transport'
    }
]

@app.route('/multiprot/api/v1.0/proteins/<int:protein_id>', methods=['GET'])
def get_protein(protein_id):
    protein = [protein for protein in proteins if protein['id'] == protein_id]
    if len(protein) == 0:
        abort(404)
    return jsonify({'protein': protein[0]})

@app.route('/multiprot/api/v1.0/proteins', methods=['POST'])
@auth.login_required
def create_protein():
    if not request.json or not 'name' in request.json:
        abort(400)
    protein = {
        'id': proteins[-1]['id'] + 1,
        'name': request.json['name'],
        'function': request.json.get('function', ""),
        'code': request.json.get('code', "")
    }
    proteins.append(protein)
    return jsonify({'protein': protein}), 201

@app.route('/multiprot/api/v1.0/proteins/<int:protein_id>', methods=['PUT'])
@auth.login_required
def update_protein(protein_id):
    protein = [protein for protein in proteins if protein['id'] == protein_id]
    if len(protein) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'function' in request.json and type(request.json['function']) is not str:
        abort(400)
    if 'code' in request.json and type(request.json['code']) is not str:
        abort(400)
    protein[0]['name'] = request.json.get('name', protein[0]['name'])
    protein[0]['function'] = request.json.get('function', protein[0]['function'])
    protein[0]['code'] = request.json.get('code', protein[0]['code'])
    return jsonify({'protein': protein[0]})

@app.route('/multiprot/api/v1.0/proteins/<int:protein_id>', methods=['DELETE'])
@auth.login_required
def delete_protein(protein_id):
    protein = [protein for protein in proteins if protein['id'] == protein_id]
    if len(protein) == 0:
        abort(404)
    proteins.remove(protein[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def make_public_protein(protein):
    new_protein = {}
    for field in protein:
        if field == 'id':
            new_protein['uri'] = url_for('get_protein', protein_id=protein['id'], _external=True)
        else:
            new_protein[field] = protein[field]
    return new_protein

@app.route('/multiprot/api/v1.0/proteins', methods=['GET'])
def get_proteins():
    return jsonify({'proteins': [make_public_protein(protein) for protein in proteins]})

if __name__ == '__main__':
    app.run(debug=True)