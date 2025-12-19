import logging
import os.path
import re
import sys
from logging.handlers import TimedRotatingFileHandler

from kutil.file import remove_extension_from_path, read_file
from kutil.file_extension import LOG

# Name of running service/EXE
_log_file_name = remove_extension_from_path(os.path.basename(sys.argv[0]))
_logback_map: dict[str, dict] = {}
_initialized: bool = False


OFF_LOG_LEVEL = "OFF"
LogLevels = {
    "INFO": logging.INFO,
    "WARN": logging.WARN,
    "ERROR": logging.ERROR,
    "DEBUG": logging.DEBUG,
    "FATAL": logging.FATAL,
    OFF_LOG_LEVEL: OFF_LOG_LEVEL
}


def get_logger(logger_name: str, logback_path: str, log_target_directory: str):
    """
    Used to create logger for provided logger name.

    Triggers the global logging initialization, retrieves specific
    configurations from the logback file, and sets the appropriate
    log level. If the level is set to 'OFF', the logger is disabled.
    """

    _initialize_logging(log_target_directory)

    logger = logging.getLogger(logger_name)
    logback = _get_logback(logback_path)
    level = _get_log_level(logger_name, logback)

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


def _get_logback(logback_path: str):
    """
    Used to read logging configuration file.
    Will use running process name to get
    corresponding logging config.

    If it doesn't exist then default logback
    file would be used - logback/SaveGem.json

    Utilizes an internal map to cache configuration data, preventing
    redundant file system reads.
    """

    global _logback_map

    if logback_path not in _logback_map:
        _logback_map[logback_path] = read_file(logback_path, as_json=True)

    return _logback_map.get(logback_path, {})


def _initialize_logging(log_target_directory: str):
    """
    Used to initialize logging.
    Should be executed only once.

    Sets up a TimedRotatingFileHandler with midnight rotation and
    a retention policy of 5 backup files. Configures the root logger
    with a standardized message format including timestamps and line numbers.
    """

    global _initialized

    if _initialized:
        return

    _handler = TimedRotatingFileHandler(
        os.path.join(log_target_directory, LOG.add_to(_log_file_name)),
        when="midnight",
        interval=1,
        backupCount=5,
        encoding="utf-8"
    )

    _handler.suffix = "%Y-%m-%d.log"
    _handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    _handler.setFormatter(logging.Formatter(
        f"%(asctime)s - (%(name)s:%(lineno)d) [{_log_file_name}] [%(levelname)s] : %(message)s"
    ))

    # Configure the root logger
    logging.getLogger().addHandler(_handler)
    _initialized = True
