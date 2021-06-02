import os
import sys
import time

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/utils"))
import LogModule
import Configs

# append utils path and import localization modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/localization"))
import readUltraSonicSensor
import readSensor
import directionDecisions

log = LogModule.init_logger()
config = Configs.configValues()

# log ultrasonic pin configs for debug purpose
log.debug(config.pins["sensors"]["ultrasonic"])

# initialise ultrasonicSensor module
ultrasonicSensor = readSensor.ultrasonicSensor(config.pins["sensors"]["ultrasonic"], { "mock": config.property["mock"]["isMock"] })

# initialise directiondecision module
dDecisions = directionDecisions.basicDecision(config.property["MEDHA"]["decisionMode"])

# initialise controlData
controlData = {
    "goAhead": True,
    "direction": "",
    "sensor": {
        "ultrasonic": {
            "left": 0,
            "right": 0,
            "front": 0
        }
    }
}


while controlData["goAhead"]:
    # read sensors and process here
    # initate 100ms gap since code runs faster than hardware processing.
    time.sleep(0.1)
    controlData["sensor"]["ultrasonic"]["right"] = ultrasonicSensor.getValue("right")
    time.sleep(0.1)
    controlData["sensor"]["ultrasonic"]["left"] = ultrasonicSensor.getValue("left")
    time.sleep(0.1)
    controlData["sensor"]["ultrasonic"]["front"] = ultrasonicSensor.getValue("front")
    # very simple logic for PoC -NOTE-remove/reform it after testing
    controlData["direction"] = dDecisions.decide(controlData["sensor"])
    log.debug("contolData: %s", controlData)
    log.info("Decision : %s", controlData["direction"])

    # initate 2 second gap for sensors and board to rest/re-settle
    time.sleep(2)
