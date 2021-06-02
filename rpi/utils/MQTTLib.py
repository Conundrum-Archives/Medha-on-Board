import os
import sys
import time
import datetime
import json
import paho.mqtt.client as mqtt

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi/utils"))
import LogModule
import Configs

log = LogModule.init_logger()
config = Configs.configValues()

class MQTT:

  def __init__(self, mqttClientID, onConnectMethod=None, onMessageMethod=None):
    self.client = mqtt.Client(client_id=str(mqttClientID))
    self.mqttChannel = {
      "name": "channel/" + str(mqttClientID),
      "status": "channel/" + str(mqttClientID) + "/status"
    }
    self.onConnectMethod = onConnectMethod
    self.onMessageMethod = onMessageMethod

    self.mqttClientID = mqttClientID
    log.info("MQTT Client (%s) initialised with mqttChannelName = %s", str(mqttClientID), str(self.mqttChannel["name"]))

  def onConnect(self, client, data, flag, rc):
    if rc == 0:
      # connection is established with MQTT broker/server
      log.info("MQTT Connection established [code = %s]", str(rc))

      # subscribe to the channel to recieve messages
      self.client.subscribe(self.mqttChannel["name"])
      log.info("MQTT Subscribe successful: %s", str(self.mqttChannel["name"]))
    else:
      errorCode = {
        0: "Connection successful",
        1: "Connection refused – incorrect protocol version",
        2: "Connection refused – invalid client identifier",
        3: "Connection refused – server unavailable",
        4: "Connection refused – bad username or password",
        5: "Connection refused – not authorised"
      }
      if rc in errorCode:
        log.warning("MQTT Connection failed with code %s : %s", str(rc), errorCode[rc])
      else:
        log.warning("MQTT Connection failed with code %s : unknown/unspecified error", str(rc))

    # call custom function if defined
    if self.onConnectMethod is not None: self.onConnectMethod(client, data, flag, rc)

  def onMessage(self, client, data, message):
    log.info("MQTT Message recieved")
    # log.debug("Message recieved from client: %s \n Data:\n %s \n Message:\n %s", str(client), str(data), str(message.payload))
    payloaddata = json.loads(str(message.payload.decode("utf-8")))
    log.debug("MQTT payload data %s", str(payloaddata))

    # call custom function if defined
    if self.onMessageMethod is not None: self.onMessageMethod({'client':client, 'data':data, 'message':message})

  def startCommunication(self):
    log.debug("MQTT authType set to %s", str(config.property["MQTT"]["auth"]["authType"]))
    if str(config.property["MQTT"]["auth"]["authType"]) == "password":
      self.client.username_pw_set(username=config.property["MQTT"]["auth"]["userName"], password=config.property["MQTT"]["auth"]["userPassword"])

    self.client.on_connect = self.onConnect
    self.client.on_message = self.onMessage
    # self.client.enable_logger()
    log.debug("status channel : %s", str(self.mqttChannel["status"]))
    self.client.will_set(topic=self.mqttChannel["status"], payload='{"status": "off", "timestamp": ' + str(datetime.datetime.now()) + '}')
    log.debug("MQTT library impl methods initialised")
    self.client.connect(config.property["MQTT"]["host"], config.property["MQTT"]["port"], config.property["MQTT"]["timeout"])
    log.info("MQTT Connection to broker established and listening for messages . .")
    self.client.loop_forever()









########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "MQTTLib.py")):

  # test for custom function
  def customOnConnect(*argsC):
    print("this log is from CUSTOMMETHODCUSTOMMETHOD :CONNECT")
    print(argsC)

  def customOnMessage(*argsM):
    print("this log is from CUSTOMMETHODCUSTOMMETHOD :MESSAGE")
    print(argsM)

  # init class object
  # mqttobj = MQTT(config.property["MEDHA"]["nodeID"])
  mqttobj = MQTT(mqttClientID=config.property["MEDHA"]["nodeID"], onConnectMethod=customOnConnect, onMessageMethod=customOnMessage)
  mqttobj.startCommunication()
