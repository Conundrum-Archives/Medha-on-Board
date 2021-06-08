import os
import sys
import cvDetect

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

log = LogModule.init_logger()
config = Configs.configValues()

class basicDecision:

  def __init__(self, mode):
    self.mode = mode

  def decide(self, data):
    if self.mode == "directionalDistance":
      if "ultrasonic" in data:
        # process ultrasonic values
        return sorted(data['ultrasonic'], key=data['ultrasonic'].get, reverse=True)[:1]
    elif self.mode == "linearDistance":
      if "camera" in data:
        # process camera-detected values
        face = cvDetect.face()
        faceDetected = face.detect()
        if len(faceDetected['distance']) > 1:
          #process for correct face/distance
          pass
        else:
          # when single face is detected
          dist = faceDetected["distance"][-1]
          ideal = config.property["MEDHA"]["distance"]["ideal"]
          gap = ideal - dist
          if gap > 0:
            # if exceeded the treshold
            if gap >= config.property["MEDHA"]["distance"]["lowerTreshold"]:
              # move back and maintain the gap
              return {
                "goto": "back",
                "gap": gap
              }
          elif gap <= 0:
            # if exceeded the treshold
            if -1*gap >= config.property["MEDHA"]["distance"]["upperTreshold"]:
              # move forward and match the gap
              return {
                "goto": "front",
                "gap": gap
              }
          return {
            "goto": "none",
            "gap": gap
          }




########## Mock function ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "directionDecisions.py")):
  # init class object with options
  bd = basicDecision(config.property["MEDHA"]["decisionMode"])

  bd.decide({
    "camera": 0
  })
  sys.exit(0)

  # import to pget random values
  import random
  # make randVal False if you want to pass specific values
  randVal = True
  # data for passing to decide def
  testdata = {
    "ultrasonic": {
      "left": 20 if not randVal else random.randint(0, 800),
      "right": 20 if not randVal else random.randint(0, 800),
      "front": 20 if not randVal else random.randint(0, 800)
    }
  }
  log.info("Test data given:\n%s", testdata["ultrasonic"])
  print(bd.decide(testdata))
