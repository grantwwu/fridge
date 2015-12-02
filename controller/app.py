# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import simplejson as json
from datetime import date, datetime

import getpass

from flask import Flask, request, send_file, render_template
import sqlalchemy

from prologue import makeSession, defer_create
from item import Item

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return json.dumps({ 'status' : 'success' })



#127.0.0.1:5000/itempage gets you to this method
@app.route('/itempage', methods=['GET'])
def itempage():
    return render_template('items.html')

@app.route('/add', methods=['POST'])
def add_item():
    with makeSession() as dbSession:
        label = request.form['label']
        amount = float(request.form['amount'])
        unit = request.form['unit']
        expdate = datetime.strptime(request.form['expdate'], "%m/%d/%Y")
        picture_id = int(request.form['imgid'])
        new_item = Item(label, amount, unit, expdate, picture_id)
        dbSession.add(new_item)
        dbSession.commit()
    return json.dumps({ 'status' : 'success' })

@app.route("/items", methods=['GET'])
def list_items():
    with makeSession() as dbSession:
        items = dbSession.query(Item).all()
        ret = [i.as_dict() for i in items]
    return json.dumps(ret)

@app.route("/items/<int:id>", methods=['GET', 'DELETE', 'POST'])
def item_endpoint(id):
    if request.method == 'GET':
        with makeSession() as dbSession:
            item = dbSession.query(Item).get(id)
            dbSession.commit()
            return item
    elif request.method == 'DELETE':
        with makeSession() as dbSession:
            item = dbSession.query(Item).get(id)
            dbSession.delete(item)
            dbSession.commit()
            return json.dumps({ 'status' : 'success' })
    elif request.method == 'POST':
        with makeSession() as dbSession:
            item = dbSession.query(Item).get(id)
            amount = float(request.form['amount'])
            unit = request.form['unit']
            item.amount = amount
            item.unit = unit
            dbSession.commit()
            return json.dumps({ 'status' : 'success' })


@app.route("/weigh", methods=['GET'])
def weight():
    return json.dumps({ 'weight' : bb.getaverageweight(5) })

imgID = 0

@app.route("/take_picture", methods=['POST'])
def take_picture():
    global imgID
    #Increment imgID counter
    imgID += 1

    # File to write to
    image_file = "../../images/img" + str(imgID) + ".png"

    tp.write_image(image_file)

    return json.dumps({ 'image_id' : imgID })

@app.route("/pictures/<int:picture_id>/", methods=['GET'])
def get_picture(picture_id):
    return send_file('../../images/img' + str(picture_id) + '.png')

def init_camera_and_scale():
    from takepic import Takepic
    from wiiweight import WiiWeight
    global tp
    tp = Takepic(0)
    global bb
    bb = WiiWeight()
    bb.calibrate()

def fake_camera_and_scale():
    global tp
    global bb
    tp = FakeTP()
    bb = FakeWiiWeight()

class FakeTP(object):
    def __init__(self):
        pass
    def write_image(self, filename):
        pass

class FakeWiiWeight(object):
    def __init__(self):
        pass
    def getaverageweight(self, readings):
        return 1.0

if __name__ == "__main__":
    defer_create()
    fake_camera_and_scale()
#    init_camera_and_scale()

    app.run(debug=True)#, host='0.0.0.0')
