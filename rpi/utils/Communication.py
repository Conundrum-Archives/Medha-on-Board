import os
import sys
import json
import MQTTLib
import datetime

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/utils"))
import LogModule
import Configs

log = LogModule.init_logger()
config = Configs.configValues()

class communicate:

    def __init__(self, mode=config.property["MEDHA"]["connectionMode"]):
        modes = ["MQTT"]
        if mode not in modes:
            log.error("Unknown connection mode passed: %s", mode)
            log.info("Available modes: %s", str(modes))
            raise Exception("Unknown connection mode passed {}".format(mode))

        self.mode = mode

        if self.mode == "MQTT":
            self.mqttobj = MQTTLib.MQTT(mqttClientID=config.property["MEDHA"]["nodeID"], onConnectMethod=self.handleMQTTConnect, onMessageMethod=self.handleMQTTMessage)

    def buildMessage(self, ref, message):
        return json.dumps({
            "timestamp": str(datetime.datetime.now()),
            "ref": ref,
            "message": message
        }, separators=(',', ':'))

    def sendMessage(self, ref, message):
        self.mqttobj.publishMsg(self.buildMessage(ref, message))

    def sendStartup(self, message={
        "status": "on"
    }):
        self.mqttobj.publishMsg(message=self.buildMessage("startup", message), topic="status")

    def handleMQTTConnect(self, *args):
        log.info("MQTT connection is successful")
        log.debug(args)

    def handleMQTTMessage(self, data):
        log.info("MQTT message: %s", data)

    def listenerMQTT(self):
        self.mqttobj.startCommunication()












########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "Communication.py")):
    cm = communicate()
    cm.sendMessage("testmodule", "testmsg")
    import time
    time.sleep(5)
