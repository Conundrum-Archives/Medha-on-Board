import os
import sys

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





########## Mock function ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "directionDecisions.py")):
  # init class object with options
  bd = basicDecision(config.property["MEDHA"]["decisionMode"])

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
