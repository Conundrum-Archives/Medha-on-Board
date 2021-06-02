import os
import sys
import time
import sched

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
import LogModule
import Configs

# initialize logger and config modules
log = LogModule.init_logger()
config = Configs.configValues()


class basicChecks:

  bgTask_Sched = sched.scheduler(time.time, time.sleep)

  def __init__(self, period):
    self.period = period

  def basicChecks1(self):
    log.info("starting startBackgroundTasks method as a schedule every %s sec", self.period)
    self.bgTask_Sched.enter(self.period, 1, self._basicChecks1, (self.bgTask_Sched,))
    self.bgTask_Sched.run()

  def _basicChecks1(self, bgTaskSched):
    log.debug("[BG-JOB::basicChecks1] running basicChecks1")
    # do the checks/actions
    self.bgTask_Sched.enter(self.period, 1, self._basicChecks1, (bgTaskSched,))
    log.debug("[BG-JOB::basicChecks1] finished basicChecks1. Re-scheduled the task again")





########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "basicChecks.py")):
  # init class object with options
  bgtime = 2  # in seconds
  bc = basicChecks(bgtime)

  # check execution
  log.info("basicChecks is executing from MOCK run")
  bc.basicChecks1()
