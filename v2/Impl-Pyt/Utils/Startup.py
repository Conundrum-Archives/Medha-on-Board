from time import sleep, time
import sched
from jsonschema import validate
from Config.Settings import Schema, Config
from Utils.SignalHandler import Handle

schema = Schema()
config = Config()


class Validation():

    # def __init__(self):
    #     pass

    def properties(self):
        ret_data = {"status": False, "message": ""}
        try:
            validate(instance=config.property, schema=schema.schema_properties)
            ret_data["status"] = True
            ret_data["message"] = "Successfully Validated properties file"
        except Exception as e:
            ret_data["status"] = False
            ret_data["message"] = "Error validating properties file. Error::\n{err}".format(err=str(e))
        return ret_data


class Init():
    def __init__(self, logger):
        self.log = logger
        self.background_task1_interval = int(config.values["background_tasks"]["background_task1_interval"])

    def _background_task1(self, sc):
        self.log.info("executing bgtask1")
        sc.enter(self.background_task1_interval, 1, self._background_task1, (sc,))

    def background_task1(self):
        sc = sched.scheduler(time, sleep)
        self.log.debug("Background tasks starting now.")
        sc.enter(self.background_task1_interval, 1, self._background_task1, (sc,))
        sc.run()

    def register_sigint_handler(self, logger):
        Handle(logger)
