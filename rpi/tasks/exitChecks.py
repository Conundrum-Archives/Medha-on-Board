import os
import sys
import atexit

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

log = LogModule.init_logger()
config = Configs.configValues()

if not config.property["mock"]["isMock"]:
    import RPi.GPIO as GPIO
    GPIO.setmode( GPIO.BOARD )

class exitChecks:
    def __init__(self):
        pass

    def atExitCheck1(self):
        log.info("[atexit::atExitCheck1] stopping and exiting Medha")
        # clear GPIO pins
        if not config.property["mock"]["isMock"]:
            log.debug("cleaning up GPIO pins")
            GPIO.cleanup()
        log.info("MEDHA message:\nSee you soon! Happy Exploration :)")





########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "exitChecks.py")):
    # init class object with options
    ec = exitChecks()

    # define atExit action
    atexit.register(ec.atExitCheck1)
