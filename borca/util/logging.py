import logging


def createLogger(name: str, level: int) -> logging.Logger:

    logger = logging.getLogger(name=name)
    loggingLevel = logging.INFO

    if level == 0:
        loggingLevel = logging.ERROR
    elif level == 2:
        loggingLevel = logging.DEBUG

    logger.setLevel(loggingLevel)
    ch = logging.StreamHandler()
    ch.setLevel(loggingLevel)
    ch.setFormatter(logging.Formatter('%(levelname)s %(name)s - %(message)s'))
    logger.addHandler(ch)

    return logger
