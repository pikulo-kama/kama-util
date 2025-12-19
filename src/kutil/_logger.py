import logging
from logging import NullHandler


def get_logger(name: str):
    """
    Creates and returns a logger instance with a NullHandler attached.

    In a library context, attaching a NullHandler ensures that no 'No handlers
    could be found' warnings are issued if the consuming application has not
    configured logging. The application retains full control over log
    formatting and destination.
    """

    logger = logging.getLogger(name)
    logger.addHandler(NullHandler())

    return logger
