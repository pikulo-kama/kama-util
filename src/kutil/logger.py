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
    """

    global _logback_map

    if logback_path not in _logback_map:
        _logback_map[logback_path] = read_file(logback_path, as_json=True)

    return _logback_map.get(logback_path, {})


def _initialize_logging(log_target_directory: str):
    """
    Used to initialize logging.
    Should be executed only once.
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
