import simplejson as json
import datetime

from flask import Flask, request
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
psql_engine = create_engine('postgresql://grantwu:yourmom@localhost/main')
Session = sessionmaker(bind=psql_engine)

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'Item'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer)
    unit = Column(String) # Todo: Change to enum
    expiration = Column(Date)

    def __init__(self, name, amount, unit, expiration):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.expiration = expiration

    def as_dict(self):
        return { 'name' : self.name,
                 'amount' : self.amount,
                 'unit' : self.unit,
                 'expiration' :
                  { 'year' : self.expiration.year,
                    'month' : self.expiration.month,
                    'day' : self.expiration.day, }
               }

Base.metadata.create_all(psql_engine)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "Hello World!"

@app.route("/add", methods=['POST'])
def add_item():
    dbSession = Session()
    name = request.form['name']
    amount = request.form['amount']
    unit = request.form['unit']
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    print(name, amount, unit, year, month, day)
    new_item = Item(name, amount, unit, datetime.date(year, month, day))
    dbSession.add(new_item)
    dbSession.commit()
    return json.dumps({ 'status' : 'success' })

@app.route("/items", methods=['GET'])
def list_items():
    dbSession = Session()
    items = dbSession.query(Item).all()
    ret = [i.as_dict() for i in items]
    return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)
