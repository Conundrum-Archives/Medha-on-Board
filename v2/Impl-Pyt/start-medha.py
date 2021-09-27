from time import sleep
import gc
import threading
from Config.Settings import Config
import Utils.LogModule as Logger


# init Config
config = Config()

# init Logger
log = Logger.init_logger(config.property["logger"])

# threads list
threads_list = {}

# validate settings and other necessary stuffs
try:
    from Utils.Startup import Validation
    vd = {"status":False}
    while(not vd["status"]):
        if ("message" in vd):
            log.error(vd["message"])
            retryIn = (config.property["systemInfo"]["settings"]["retryValidationInSec"] if (type(config.property["systemInfo"]["settings"]["retryValidationInSec"]) is int) else 10) or 10
            log.info("Resolve the validation check to proceed. Checking after {time} sec".format(time=(retryIn if (type(retryIn) is int) else 10)))
            sleep(retryIn)
        vd = Validation().properties()
    log.debug(vd["message"])
except Exception as e:
    log.error("Exception occured during validation of settings:: %s", str(e))
    log.warning("Exiting system now.")
finally:
    # clean validation methods imported
    gc.collect()


# init bg tasks at startup
try:
    from Utils.Startup import Init
    init = Init(log)
    threads_list['backgroundtasks'] = threading.Thread(target=init.background_task1, args=(), daemon=False)
    threads_list['backgroundtasks'].start()
    log.debug("backgroundtasks thread started successfully.")

    # register sigint handler
    init.register_sigint_handler(log)
except Exception as e:
    log.error("Exception occured during initialization of background tasks during startup:: %s", str(e))
    log.warning("Exiting system now.")
finally:
    # clean validation methods imported
    gc.collect()

log.debug("Initialization successful. Starting main loop now.")

try:
    from Local.Main import Process
    process = Process(log)

    #create thread for main loop
    threads_list["mainloop"] = threading.Thread(target=process.start, args=(), daemon=False)
    threads_list["mainloop"].start()
    log.debug("main loop thread started successfully.")
except Exception as e:
    log.error("Exception occured during starting of mainloop thread:: %s", str(e))
    log.warning("Exiting system now.")
finally:
    # clean validation methods imported
    gc.collect()

log.debug("Threads running successfully.")