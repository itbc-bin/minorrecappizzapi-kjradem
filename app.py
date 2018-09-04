from flask import Flask, jsonify, request

app = Flask(__name__)

pizzaDB = [
            {'name': 'Margaritha'},
            {'name': 'Hawaii'},
            {'name': 'Hawaii met extra ananas voor Sjors'},
            {'name': 'Salami'}
          ]


@app.route("/", methods=['GET'])
def getPizza():
    return jsonify({'pizzaDB':pizzaDB})


if __name__ == '__main__':
    app.run(debug=True)
