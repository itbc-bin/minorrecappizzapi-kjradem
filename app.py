from flask import Flask, jsonify, request

app = Flask(__name__)

pizzaDB = [
            {'name': 'Margaritha', 'plebian': True},
            {'name': 'Hawaii', 'acceptabel': True},
            {'name': 'Hawaii met extra ananas voor Sjors', 'acceptabel': True},
            {'name': 'Salami', 'Kosher': False},
            {'name': 'Quattro Formaggi', 'si si': True},
            {'name': 'Chocolade met extra Nutella', 'melts': True}
          ]


@app.route("/", methods=['GET'])
def get_pizza():
    return jsonify({'pizzaDB': pizzaDB})


@app.route('/<string:name>', methods=['GET'])
def get_one_pizza(name):
    result = [pizza for pizza in pizzaDB if pizza['name'] == name]
    return jsonify({'pizzaDB': result})


if __name__ == '__main__':
    app.run(debug=True)
