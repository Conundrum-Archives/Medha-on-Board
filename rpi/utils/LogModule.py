import logging
import Configs
import paho.mqtt.client as mqtt

config = Configs.configValues()

# myHandler = MQTTHandler(hostname, topic)
# myHandler.setLevel(logging.INFO)
# myHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s'))
# logger.addHandler(myHandler)

def init_logger():
    # init log module
    logging.basicConfig(
        format='%(asctime)-15s - %(levelname)8s - %(module)10s - %(message)s',
        level=logging.DEBUG,
        datefmt='%m/%d/%Y %I:%M:%S.%p',
        handlers=[
            logging.FileHandler("medha.log"),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)

    mqttLogHandler = MQTTHandler()
    mqttLogHandler.setLevel(logging.DEBUG)
    mqttLogHandler.setFormatter(logging.Formatter('{"timestamp": "%(asctime)s","level": "%(levelname)s", "log": "%(message)s"}'))
    logger.addHandler(mqttLogHandler)

    return logger

class MQTTHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a MQTT server to a topic.
    """
    def __init__(self):
        logging.Handler.__init__(self)
        self.mqttClientID = config.property["MEDHA"]["nodeID"]
        self.channel = "channel/" + self.mqttClientID + "/logs"
        self.client = mqtt.Client(client_id=self.mqttClientID, clean_session=False)
        if str(config.property["MQTT"]["auth"]["authType"]) == "password":
            self.client.username_pw_set(username=config.property["MQTT"]["auth"]["userName"], password=config.property["MQTT"]["auth"]["userPassword"])

        if config.property["MQTT"]["tls"]:
            self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.connect(config.property["MQTT"]["host"], config.property["MQTT"]["port"], config.property["MQTT"]["timeout"])

    def emit(self, record):
        """
        Publish a single formatted logging record to a broker, then disconnect
        cleanly.
        """
        msg = self.format(record)
        self.client.publish(topic=self.channel, payload=msg, qos=1)
