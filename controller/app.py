import simplejson as json
import datetime

from flask import Flask, request
import sqlalchemy

from prologue import makeSession
from item import Item

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return json.dumps({ 'status' : 'success' })

@app.route("/add", methods=['POST'])
def add_item():
    with makeSession() as dbSession:
        label = request.form['label']
        amount = float(request.form['amount'])
        unit = request.form['unit']
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        picture_id = int(request.form['picture_id'])
        new_item = Item(label, amount, unit,
                        datetime.date(year, month, day), picture_id)
        dbSession.add(new_item)
        dbSession.commit()
    return json.dumps({ 'status' : 'success' })

@app.route("/items", methods=['GET'])
def list_items():
    with makeSession() as dbSession:
        items = dbSession.query(Item).all()
        ret = [i.as_dict() for i in items]
    return json.dumps(ret)

@app.route("/items/<int:id>", methods=['GET'])
def get_item(id):
    with makeSession() as dbSession:
        item = dbSession.query(Item).get(id)
        return item

@app.route("/weigh", methods=['GET'])
def weight():
    # TODO: Finish this
    pass

@app.route("/take_picture", methods=['POST'])
def take_picture():
    # TODO: Finish this
    # Should return a picture ID
    pass

@app.route("/pictures/<int:picture_id>/", methods=['GET'])
def get_picture(picture_id):
    pass

if __name__ == "__main__":
    defer_create()
    app.run(debug=True)
