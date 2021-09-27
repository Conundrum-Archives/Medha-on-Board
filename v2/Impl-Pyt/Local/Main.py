from time import sleep

class Process():

    def __init__(self, logger):
        self.log = logger

    def start(self):
        while True:
            self.log.info("main loop -> looped")
            sleep(10)