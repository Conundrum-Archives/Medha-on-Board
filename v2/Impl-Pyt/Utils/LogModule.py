import logging

def init_logger(config):
    LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    # add log channels based on config
    handlers = []
    if ("FILE" in config["channels"]):
        handlers.append(logging.FileHandler(config["channels"]["FILE"]["name"]))
    if ("CONSOLE" in config["channels"]):
        handlers.append(logging.StreamHandler())

    # init log module
    logging.basicConfig(
        format='%(asctime)-15s - %(levelname)8s - %(module)10s - %(message)s',
        level=LEVELS[config["level"]],
        datefmt='%m/%d/%Y %I:%M:%S.%p',
        handlers=handlers
    )

    return logging.getLogger(__name__)
