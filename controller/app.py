import simplejson as json
import datetime
from contextlib import contextmanager
import getpass
import cv2
import sys
sys.path.insert(0, '/home/matt/Downloads/wiibalance/cwiid/python/build/lib.linux-x86_64-2.7/')
import cwiid
import time
import wiiweight

from flask import Flask, request
from item import Item
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)

psql_engine = create_engine('postgresql://' + getpass.getuser() +
                            ':15291@localhost/main')
Session = sessionmaker(bind=psql_engine)
#Session = scoped_session(session_factory)

import item

item.Base.metadata.create_all(psql_engine)

#Builtin webcam for laptop is 0, usb cam is 1
camera_port = 0
#image ID
imgID = -1
#Initialize camera
webcam = cv2.VideoCapture(camera_port)



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
    dbSession = Session()
#    with dbSession() as dbSession:
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
#    with dbSession() as dbSession:
    dbSession = Session()
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

def get_image():
    #Gets image from webcam
    retval, img = webcam.read()
    return img

@app.route("/take_picture", methods=['POST'])
def take_picture():
    # TODO: Finish this
    # Should return a picture ID
    global webcam
    global imgID

    #throw away frames for camera adjustment
    ramp_frames = 30

    #Increment imgID counter
    imgID += 1

    for i in xrange(ramp_frames):
        temp = get_image()

    print("Taking Image...")

    captureimg = get_image()

    #File to write to
    file = "../../images/img" + str(imgID) + ".png"

    cv2.imwrite(file, captureimg)

    # Release webcam for additional pictures
    del (webcam)

    return imgID
    pass

@app.route("/pictures/<int:picture_id>/", methods=['GET'])
def get_picture(picture_id):
    pass

take_picture()
#wiiweight.get_weight()
if __name__ == "__main__":
    app.run(host='0.0.0.0')
#    app.run(debug=True)
