import os
import logging.config
import logging.handlers

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
logging.config.fileConfig('{}/logging.config'.format(CURR_DIR))


def get_default_logger(name):
    logger = logging.getLogger(name)
    return logger
