import simplejson as json
import datetime

import getpass
# import cv2
import sys
sys.path.insert(0, '/home/matt/Downloads/wiibalance/cwiid/python/build/lib.linux-x86_64-2.7/')
# import cwiid
import time
from datetime import datetime, date
# import wiiweight

from flask import Flask, request, render_template
import sqlalchemy

from prologue import makeSession, defer_create
from item import Item

#Builtin webcam for laptop is 0, usb cam is 1
camera_port = 0
#image ID
imgID = -1
#Initialize camera
# webcam = cv2.VideoCapture(camera_port)

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
        print request.form
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
        print ret
    return json.dumps(ret)

@app.route("/items/<int:id>", methods=['GET','DELETE'])
def get_or_delete_item(id):
    if request.method == 'GET':
        with makeSession() as dbSession:
            item = dbSession.query(Item).get(id)
            return item
    else:
        with makeSession() as dbSession:
            item = dbSesion.query(Item).get(id)
            dbSession.delete(item)
            return json.dumps({'status':'success'})

@app.route("/weigh", methods=['GET'])
def weight():
    # TODO: Finish this
    pass

# def get_image():
    #Gets image from webcam
#    retval, img = webcam.read()
#    return img

# @app.route("/take_picture", methods=['POST'])
# def take_picture():
#     # TODO: Finish this
#     # Should return a picture ID
#     global webcam
#     global imgID
#
#     #throw away frames for camera adjustment
#     ramp_frames = 30
#
#     #Increment imgID counter
#     imgID += 1
#
#     for i in xrange(ramp_frames):
#         temp = get_image()
#
#     print("Taking Image...")
#
#     captureimg = get_image()
#
#     #File to write to
#     file = "../../images/img" + str(imgID) + ".png"
#
#     cv2.imwrite(file, captureimg)
#
#     # Release webcam for additional pictures
#     del (webcam)
#
#     return imgID
#     pass

@app.route("/pictures/<int:picture_id>/", methods=['GET'])
def get_picture(picture_id):
    pass

#take_picture()
#wiiweight.get_weight()

if __name__ == "__main__":
    defer_create()
    app.run(debug=True)
