import json
from flask import Flask, request
app = Flask(__name__)

items = {}

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"


@app.route("/add", methods=['POST'])
def add_item():
    name = request.form['name']
    amount = request.form['amount']
    unit = request.form['unit']
    expiration = request.form['expiration']
    items[name] = { 'amount' : amount,
                    'unit' : unit,
                    'expiration' : expiration, }
    return ""

@app.route("/items", methods=['GET'])
def list_items():
    return json.dumps(items)

if __name__ == "__main__":
    app.run()
