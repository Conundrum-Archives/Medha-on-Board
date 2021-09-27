import os
import sys
import json
import socket

# append utils path and import utils modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils"))
from Communication import communicate
import LogModule
import Configs

# initialize logger and config modules
log = LogModule.init_logger()
config = Configs.configValues()
comm = communicate()

"""startup tasks when starting main-loop"""

def initialize1():
    """initial tasks - set envfile and send message of startup"""

    hostname = socket.gethostname()
    data = {
        "pid": os.getpid(),
        "hostname": hostname,
        "ip": socket.gethostbyname(hostname)
    }
    # delete if file exist during run time
    if os.path.exists(config.property["MEDHA"]["envFile"]):
        os.remove(config.property["MEDHA"]["envFile"])
    with open(config.property["MEDHA"]["envFile"], 'w') as f:
        json.dump(data, f)

    # send message that medha is started
    comm.sendStartup()







########## Mock functions ##########
if (( config.property["mock"]["isMock"] ) and (__file__ == "startActivity.py")):
    # init class object with options

    # check execution
    log.info("basicChecks is executing from MOCK run")
    initialize1()
