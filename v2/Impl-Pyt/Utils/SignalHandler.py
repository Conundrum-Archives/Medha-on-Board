import sys
import signal

class Handle():
    def __init__(self, logger):
        self.log = logger
        signal.signal(signal.SIGINT, self.sigint_handler)

    def sigint_handler(self):
        self.log.warning("SIGINT detected")
        sys.exit(0)