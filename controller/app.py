import simplejson as json
import datetime
from contextlib import contextmanager
import getpass

from flask import Flask, request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

psql_engine = create_engine('postgresql://' + getpass.getuser() +
                            ':15291@localhost/main')
session_factory = sessionmaker(bind=psql_engine)
Session = scoped_session(session_factory)

Base = declarative_base()

Base.metadata.create_all(psql_engine)

@contextmanager
def dbSession():
    dbSession = Session()
    try:
        yield dbSession
    finally:
        dbSession.close()

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

@app.route("/add", methods=['POST'])
def add_item():
    with dbSession() as dbSession:
        label = request.form['label']
        amount = request.form['amount']
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
    with dbSession() as dbSession:
        items = dbSession.query(Item).all()
        ret = [i.as_dict() for i in items]
    return json.dumps(ret)

@app.route("/items/<int:id>", methods=['GET'])
def get_item(id):
    dbSession = Session()

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
    app.run(debug=True)
