import cv2
import sys
import math
import os
import site
import os.path
import mlify.detect.face as df

"""class for interfacing detect functionality from medha-mlify library"""

class face:
    """face detector class interface for medha-mlify face detector"""

    def __init__(self, mode="capture", imagefile="", capturedevice=0):
        # available modes of reading image - capture from cam or read from image file
        modes = [ "capture", "imagefile" ]

        # pre-check for params
        if mode not in modes:
            raise Exception("invalid mode value passed: {mode}".format(mode=mode))
        elif mode == "imagefile" and ( imagefile == "" or not os.path.isfile(imagefile) ):
            raise Exception("invalid imagefile value passed or imagefile does not exist: {imagefile}".format(imagefile=imagefile))

        if mode == "capture":
            # initiate camera device for capturing
            self.capture = cv2.VideoCapture(capturedevice)
        elif mode == "imagefile":
            self.imagefile = imagefile

        # simpleFaceDetect() is method from medha-mlify
        self.sfd = df.simpleFaceDetect()
        self.mode = mode

    def captureImage(self):
        # capture image from camera device and return the frame
        __, frame = self.capture.read()
        return frame

    def detect(self):
        if self.mode == "capture":
            image = self.captureImage()
        elif self.mode == "imagefile":
            image = cv2.imread(self.imagefile)
        # return detected data of captured frame to caller
        return self.sfd.detect(image)
