import os
import sys
import time
import json

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/utils"))
import LogModule
import Configs
import MQTTLib as MQTT

# append utils path and import localization modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/localization"))
import actuateMotors

log = LogModule.init_logger()
config = Configs.configValues()
am = actuateMotors.setMotors()

log.info("starting mqttcontrol_ON_BOARD module.\nNODEID: %s", str(config.property["MEDHA"]["nodeID"]))

def motorControlMiddleware(args):
        payloadData = json.loads(args["message"].payload.decode("utf-8"))
        log.debug(payloadData)
        if "actionMode" in payloadData and "setMotion" in payloadData:
                am.motorMotion(payloadData["setMotion"]["value"])

mqttobj = MQTT.MQTT(config.property["MEDHA"]["nodeID"], onMessageMethod=motorControlMiddleware)
mqttobj.startCommunication()
