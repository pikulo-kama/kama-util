import logging
import os.path
import re
import sys
from logging import NullHandler
from logging.handlers import TimedRotatingFileHandler

from kutil.file import remove_extension_from_path, read_file
from kutil.file_type import LOG

# Name of running service/EXE
_log_file_name = remove_extension_from_path(os.path.basename(sys.argv[0]))
_logback: dict[str, str] = {}


OFF_LOG_LEVEL = "OFF"
LogLevels = {
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "DEBUG": logging.DEBUG,
    "FATAL": logging.FATAL,
    OFF_LOG_LEVEL: OFF_LOG_LEVEL
}

# Use null handler by default.
# This would later be overridden when file
# logger would be initialized.
logging.getLogger().addHandler(NullHandler())


def get_logger(logger_name: str):
    """
    Used to create logger for provided logger name.

    Triggers the global logging initialization, retrieves specific
    configurations from the logback file, and sets the appropriate
    log level. If the level is set to 'OFF', the logger is disabled.
    """

    logger = logging.getLogger(logger_name)
    level = _get_log_level(logger_name, _logback or {})

    if level == OFF_LOG_LEVEL:
        logger.disabled = True

    else:
        logger.setLevel(level)

    return logger


def _get_log_level(logger_name: str, logback: dict):
    """
    Used to query logback and get configured log level for provided log name.
    If log level is not configured 'INFO' would be used as default.

    Maps the string level from the configuration dictionary to standard
    logging constants defined in the LogLevels map.
    """

    level = logback.get(logger_name)

    if level is not None:
        return LogLevels[level]

    return logging.INFO


def initialize_logging(log_target_directory: str, logback_path: str):
    """
    Used to initialize logging.
    Should be executed only once.

    Sets up a TimedRotatingFileHandler with midnight rotation and
    a retention policy of 5 backup files. Configures the root logger
    with a standardized message format including timestamps and line numbers.
    """

    global _logback

    if os.path.exists(logback_path):
        _logback = read_file(logback_path, as_json=True)

    log_handler = TimedRotatingFileHandler(
        os.path.join(log_target_directory, LOG.add_extension(_log_file_name)),
        when="midnight",
        interval=1,
        backupCount=5,
        encoding="utf-8"
    )

    log_handler.suffix = "%Y-%m-%d.log"
    log_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    log_handler.setFormatter(logging.Formatter(
        f"%(asctime)s - (%(name)s:%(lineno)d) [{_log_file_name}] [%(levelname)s] : %(message)s"
    ))

    # Configure the root logger
    # using new handler.
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    root_logger.addHandler(log_handler)
