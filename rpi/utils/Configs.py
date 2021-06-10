import json
import os.path

class configValues:

    PINS_FILE = "pins.json"
    PROPERTY_FILE = "properties.json"

    def __init__(self):

        # read and init properties file
        if os.path.exists(self.PROPERTY_FILE):
            # check in actual location
            with open(self.PROPERTY_FILE) as property:
                self.property = json.load(property)
        elif os.path.exists("../" + self.PROPERTY_FILE):
            # check in mock path
            with open("../" + self.PROPERTY_FILE) as property:
                self.property = json.load(property)
        elif os.path.exists("../rpi/" + self.PROPERTY_FILE):
            # check in mock path
            with open("../rpi/" + self.PROPERTY_FILE) as property:
                self.property = json.load(property)
        else:
            raise Exception("File not found in actual, prototypes and mock paths: " + self.PROPERTY_FILE)


        # read and init pins file
        if os.path.exists(self.PINS_FILE):
            # check in actual location
            with open(self.PINS_FILE) as pins:
                self.pins = json.load(pins)
        elif os.path.exists("../" + self.PINS_FILE):
            # check in mock path
            with open("../" + self.PINS_FILE) as pins:
                self.pins = json.load(pins)
        elif os.path.exists("../rpi/" + self.PINS_FILE):
            # check in mock path
            with open("../rpi/" + self.PINS_FILE) as pins:
                self.pins = json.load(pins)
        else:
            raise Exception("File not found in actual and mock paths: " + self.PINS_FILE)
