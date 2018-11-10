import logging

mylogger = logging.getLogger("my")
mylogger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def critical(msg, *args, **kwargs):
    mylogger.critical(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    mylogger.error(msg, *args, **kwargs)


def exception(msg, *args, exc_info=True, **kwargs):
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg, *args, **kwargs):
    mylogger.warning(msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    warning(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    mylogger.info(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    mylogger.debug(msg, *args, **kwargs)

