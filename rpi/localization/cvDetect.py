import cv2
import sys
import math
import os
import site
import os.path
import mlify.detect.face as df

class face:
  
  def __init__(self, mode="capture", imagefile="", capturedevice=0):
    modes = [ "capture", "imagefile" ]

    # pre-check for params
    if mode not in modes:
      raise Exception("invalid mode value passed: {mode}".format(mode=mode))
    elif mode == "imagefile" and ( imagefile == "" or not os.path.isfile(imagefile) ):
      raise Exception("invalid imagefile value passed or imagefile does not exist: {imagefile}".format(imagefile=imagefile))

    if mode == "capture":
      self.capture = cv2.VideoCapture(capturedevice)
    elif mode == "imagefile":
      self.imagefile = imagefile

    self.sfd = df.simpleFaceDetect()
    self.mode = mode

  def captureImage(self):
    __, frame = self.capture.read()
    return frame

  def detect(self):
    if self.mode == "capture":
      image = self.captureImage()
    elif self.mode == "imagefile":
      image = cv2.imread(self.imagefile)
    return self.sfd.detect(image)
