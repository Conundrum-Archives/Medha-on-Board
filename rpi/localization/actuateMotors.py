import os
import sys

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

# import Rpi modules if not mock
if (( not config.property["mock"]["isMock"] )):
  import RPi.GPIO as GPIO
  GPIO.setmode( GPIO.BOARD )

# initialize logger and config modules
log = LogModule.init_logger()
config = Configs.configValues()


class setMotors:

  """
    motion table values for controling motor driver. refer to motor-driver table for values.
  """

  motionTable = {
    "stop": {
      "motorL": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" },
      "motorR": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" }
    },
    "front": {
      "motorL": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH" },
      "motorR": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH" }
    },
    "back": {
      "motorL": { "a": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" },
      "motorR": { "a": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" }
    },
    "right": {
      "motorL": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH" },
      "motorR": { "a": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" }
    },
    "left": {
      "motorL": { "a": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH", "b": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW" },
      "motorR": { "a": GPIO.LOW if not config.property["mock"]["isMock"] else "LOW", "b": GPIO.HIGH if not config.property["mock"]["isMock"] else "HIGH" }
    }
  }

  def __init__(self):
    if (not config.property["mock"]["isMock"]):
      # initiate cleanup if any and set GPIO board mode
      GPIO.cleanup()
      GPIO.setmode( GPIO.BOARD )

      # set pin number for each motor control pins and set as OUT mode
      GPIO.setup( config.pins["motorL"]["a"], GPIO.OUT )
      GPIO.setup( config.pins["motorL"]["b"], GPIO.OUT )
      GPIO.setup( config.pins["motorR"]["a"], GPIO.OUT )
      GPIO.setup( config.pins["motorR"]["b"], GPIO.OUT )
    log.debug("motor control pins initialised for actuation")

  def motorMotion(self, motionName):
    # check if proper motionName is provided in message passed.
    if motionName not in self.motionTable:
      log.error("unknown motionName: %s", motionName)
    else:
      log.info("Motor motion set to : %s", motionName)
      motionSet = self.motionTable[motionName]
      for motor in motionSet:
        for pin in motionSet[motor]:
          if not config.property["mock"]["isMock"]:
            GPIO.output( config.pins[motor][pin], motionSet[motor][pin] )
            log.debug("setting motor control pin %s to %s", str(config.pins[motor][pin]), str(motionSet[motor][pin]))
          else:
            log.info("[MOCK] PINOUTPUT: [ %s %s ]", config.pins[motor][pin], motionSet[motor][pin])









########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "actuateMotors.py")):
  import random
  numOfTimes = 10
  motions = ["stop","front","back","right","left"]
  # init class object with options
  am = setMotors()
  for t in range(numOfTimes):
    am.motorMotion(motions[random.randint(0, 4)])
    log.info("\n\n\n\n")
