import signal
import os
import sys

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

log = LogModule.init_logger()
config = Configs.configValues()

class signalHandler:
    def __init__(self):
        signal.signal(signal.SIGINT, self.SIGINT_handler)

    def SIGINT_handler(self, sig, frame):
        log.warning('SIGINT DETECTED, exiting now')
        sys.exit(0)







########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "SignalHandler.py")):
    import time

    # init class object
    signalhandler = signalHandler()
    while True:
        log.debug("did you know? everytime this is printed 1 second would have passed!")
        time.sleep(1)
