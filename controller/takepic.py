#!/usr/bin/python
import cv2


class Takepic(object):
    #Builtin webcam for laptop is 0, usb cam is 1
    #camera_port = 0

    #throw away frames for camera adjustment
    ramp_frames = 30

    def __init__( self, camera_port ):
        self.webcam = cv2.VideoCapture(camera_port)

    def get_image( self ):
        for i in xrange(self.ramp_frames):
            temp = self.webcam.read()

        retval, img = self.webcam.read()
        return img

    def write_image( self, image_path):
        file = str(image_path)
        
        cv2.imwrite(file, self.get_image() )

        
