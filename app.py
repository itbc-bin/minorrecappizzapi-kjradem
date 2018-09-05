from flask import Flask, jsonify, request

app = Flask(__name__)

pizzaDB = [
            {'name': 'Hawaii',
             'price': 8,
             'ingredients': ['Ham', 'Ananas']
            },
            {'name': 'Dr. Oetker Ristorante Dolce al Cioccolato',
             'price': 10,
             'ingredients': ['Chocoladesaus', 'Witte chocolade', 'Melkchocolade']
            },
            {'name': 'Tonno',
             'price': 10,
             'ingredients': ['Tonijn']
            }
          ]


@app.route('/', methods=['GET'])
def get_pizzas():
    return jsonify({'pizzaDB': pizzaDB})


@app.route('/add/', methods=['POST'])
def add_pizza():
    pizza = {'name': request.json['name'], 'ingredients': request.json['ingredients'], 'price': request.json['price']}
    pizzaDB.append(pizza)
    return jsonify({'pizzaDB': pizzaDB})


@app.route('/append/<string:item>/', methods=['POST'])
def append_pizza(item):
    result = [pizza for pizza in pizzaDB if pizza['name'] == item]
    for ingredient in request.json['ingredients']:
        result[0]['ingredients'].append(ingredient)
    return jsonify({'pizzaDB': pizzaDB})


@app.route('/pizza/<string:item>', methods=['GET'])
def get_pizza(item):
    result = [pizza for pizza in pizzaDB if pizza['name'] == item]
    return jsonify({'pizzaDB': result})


@app.route('/pizza/<string:item>/ingredients', methods=['GET'])
def get_ingredients(item):
    result = [pizza['ingredients'] for pizza in pizzaDB if pizza['name'] == item]
    return jsonify({'pizzaDB': result})


@app.route('/pizza/<string:item>/price', methods=['GET'])
def get_price(item):
    result = [pizza['price'] for pizza in pizzaDB if pizza['name'] == item]
    return jsonify({'pizzaDB': result})


if __name__ == '__main__':
    app.run(debug=True)
