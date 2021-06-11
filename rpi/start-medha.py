import time
import atexit
import threading
import utils.Configs as Configs
import utils.LogModule as LogModule
import utils.SignalHandler as signalHandler
import localization.readSensor as readSensor
import localization.actuateMotors as actuateMotors
import localization.directionDecisions as directionDecisions
from tasks.startActivity import initialize1
from Communication import communicate
import tasks.basicChecks as bc
import tasks.exitChecks as ec

# initialize logger, communication and config modules
log = LogModule.init_logger()
config = Configs.configValues()
comm = communicate()

# configure options
options = {
    "minDistance": 60,
    "sleep": 1,
    "bgTaskTimer": 2
}

# run background jobs if any
# define background tasks defs
def startBackgroundTasks():
    """initializes background tasks method to run tasks such as checks and monitor in background"""

    log.debug("[startBackgroundTasks] starting ")
    bc.basicChecks(options["bgTaskTimer"]).basicChecks1()
    log.info("[startBackgroundTasks] Thread started in background [ name: %s | identity: %s ]", threading.current_thread().name, threading.get_ident())


def startMainLoop(goAhead):
    """The main loop of Medha-on-Board which is main entry point to execution"""

    # init dependant modules and give a goAhead key

    # set directionDecision mode from property file
    _directionDecisions = directionDecisions.basicDecision(config.property["MEDHA"]["decisionMode"])

    # initialise motor module to control motors
    _actuateMotors = actuateMotors.setMotors()

    # init control data to handle execution based on instructions, decisions and other factors.
    controlData = {
            "goAhead": goAhead
    }

    # start loop based on control data values
    while controlData["goAhead"]:
        # process the modules here
        # example1: read camera functionality and call decision module
        # example2: read sensor data to decide whih direction to move
        log.debug("goAhead is %s.", controlData["goAhead"])

        # get decision from camera bsed on distance
        camDecision = _directionDecisions.decide({
            "camera": 0
        })
        log.info("decision from cameradecision is %s", camDecision)

        # set motor motion based on decision
        _actuateMotors.motorMotion(camDecision["goto"])

        # sleep is added to limit empty loop timing or reduce stress on processing - can be removed later when modules are imported.
        time.sleep(2)


# use this for pre-checking for any conditions like communcation, camera, sensors, etc
def initChecks():
    """
        pre-check method before starting main loop.
        example: check for instructions, power-module, etc.
    """

    return True

def startMedha():
    """set startup handlers and checks before starting main loop."""
    # check for SIGNALS
    signalhandler = signalHandler.signalHandler()

    # initialize on exit actions
    atexit.register(ec.exitChecks().atExitCheck1)

    # initialize background tasks
    basicChecksThread = threading.Thread(target=startBackgroundTasks, args=(), daemon=True).start()

    # initialize startupscript
    initialize1()

    # wait for certain initial criteria to become True
    initcheck = initChecks()
    while not initcheck:
        time.sleep(1)
        initcheck = initChecks()

    startMainLoop(goAhead=initcheck);

if __name__ == '__main__':
    startMedha()
