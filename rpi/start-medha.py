import time
import threading
import atexit
from tasks.startActivity import initializeEnvDetailsFile
import localization.readSensor as readSensor
import localization.directionDecisions as directionDecisions
import utils.LogModule as LogModule
import utils.Configs as Configs
import utils.SignalHandler as signalHandler
import tasks.basicChecks as bc
import tasks.exitChecks as ec

# initialize logger and config modules
log = LogModule.init_logger()
config = Configs.configValues()

# configure options
options = {
  "minDistance": 60,
  "sleep": 1,
  "bgTaskTimer": 2
}

# run background jobs if any
# define background tasks defs
def startBackgroundTasks():
  log.info("[startBackgroundTasks] Thread started in background [ name: %s | identity: %s ]", threading.current_thread().name, threading.get_ident())
  bc.basicChecks(options["bgTaskTimer"]).basicChecks1()



def startMainLoop(goAhead):
  # init dependant modules and give a goAhead key
  dd = directionDecisions.basicDecision(config.property["MEDHA"]["decisionMode"])
  controlData = {
      "goAhead": goAhead
  }
  while controlData["goAhead"]:
    # process the modules here
    # example1: read camera functionality and call decision module
    # example2: read sensor data to decide whih direction to move
    log.debug("goAhead is %s.", controlData["goAhead"])
    log.info("decision is %s", dd.decide({
      "camera": 0
    }))

    # sleep is added to limit empty loop timing or reduce stress on processing - can be removed later when modules are imported.
    time.sleep(2)


# use this for pre-checking for any conditions like communcation, camera, sensors, etc
def initChecks():
  return True

def startMedha():
  # check for SIGNALS
  signalhandler = signalHandler.signalHandler()

  # initialize on exit actions
  atexit.register(ec.exitChecks().atExitCheck1)

  # initialize background tasks
  basicChecksThread = threading.Thread(target=startBackgroundTasks, args=(), daemon=True).start()

  # initialize startupscript
  initializeEnvDetailsFile()

  # wait for certain initial criteria to become True
  while not initChecks(): time.sleep(1)
  startMainLoop(goAhead=True);

if __name__ == '__main__':
  startMedha()
