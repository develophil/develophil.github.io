import logging

mylogger = logging.getLogger("my")
mylogger.propagate=0
mylogger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
mylogger.addHandler(stream_hander)

# file_handler = logging.FileHandler('my.log')
# mylogger.addHandler(file_handler)

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

'''
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
'''

