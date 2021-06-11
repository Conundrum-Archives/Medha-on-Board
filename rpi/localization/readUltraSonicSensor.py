
import os
import sys
import random
import time

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

# initialize logger and config modules
log = LogModule.init_logger()
config = Configs.configValues()

# import Rpi modules if not mock
if (( not config.property["mock"]["isMock"] )):
    import RPi.GPIO as GPIO
    GPIO.setmode( GPIO.BOARD )

class readUltraSonicSensor:

    """
        sensor class to read unltrasonic sensor values
        # NOTE: This class is direct interface to GPIO pins of ultrasonic-sensor.
    """

    def __init__(self, options):
        self.usspins = config.pins["sensors"]["ultrasonic"]
        if (("mock" in options) and (options["mock"])):
            # set mock if specified and mock is passed True
            self.mock = options["mock"]
        else:
            # set the pinModes for each
            for pinName in self.usspins:
                GPIO.setup(self.usspins[pinName]["TRIG"], GPIO.OUT)
                GPIO.setup(self.usspins[pinName]["ECHO"], GPIO.IN)

    def readSensorValue(self, pinName):
        """
            returns sensor values from ultrasonic sensor.
            takes in one parameter: pinName
            returns reading from ultrasonic sensor
        """

        if not self.mock:
            # read and return sensor value
            GPIO.output(self.usspins[pinName]["TRIG"], True)
            time.sleep(0.00001)
            GPIO.output(self.usspins[pinName]["TRIG"], False)

            pulse_start = time.time()
            pulse_stop = time.time()
            while ( (GPIO.input(self.usspins[pinName]["ECHO"]) == 0) ):
                pulse_start = time.time()
            while ( (GPIO.input(self.usspins[pinName]["ECHO"]) == 1) ):
                pulse_stop = time.time()
            pulse_duration = (pulse_stop - pulse_start)
            # 17150 is half the two-way speed of sound in air in ms
            distance = pulse_duration * 17150
            return distance
        elif self.mock:
            # if mock, return mock values
            return random.randint(0, 800)










########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "readUltraSonicSensor.py")):
    # init class object with options
    rus = readUltraSonicSensor({
        "mock": config.property["mock"]["isMock"]
    })

    # check the value responses
    numOfTimes = 10
    pinToReadFrom = config.pins["sensors"]["ultrasonic"]["right01"]
    for num in range(numOfTimes):
        log.info("MOCK: PIN:%s | %s", pinToReadFrom, rus.readSensorValue(pinToReadFrom))
