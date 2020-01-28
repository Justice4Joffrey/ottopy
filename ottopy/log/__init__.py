import logging
import os
import sys

from ottopy.log.classes import (
    UTCMicroSecFormatter,
    LogLevel,
    UTCTimedRotatingFileHandler,
    WhenType)
from ottopy.log.consts import FORMATTER, RAW_FORMATTER, DEFAULT_SUFFIX

__all__ = [
    "get_logger",
    "get_raw_logger",
    "make_file_handler",
    "make_stdout_handler",
    "init_file_logger",
    "LogLevel",
    "Logger",
    "Formatter",
    "StreamHandler",
    "UTCMicroSecFormatter",
    "FORMATTER",
    "RAW_FORMATTER",
]

# unpack to help auto-import
from ottopy.read import create_dir

StreamHandler = logging.StreamHandler
Formatter = logging.Formatter
Logger = logging.Logger


def get_logger(
    name: str = "", level: int = LogLevel.INFO, propagate: bool = True
) -> Logger:
    logger = logging.getLogger(name)
    logger.propagate = propagate
    logger.setLevel(level)
    return logger


def get_raw_logger(name: str = "raw") -> Logger:
    if not name:
        raise ValueError(f"Raw logger name cannot be empty {name!r}")
    return get_logger(name, level=LogLevel.DEBUG, propagate=False)


def make_stdout_handler(
    formatter: Formatter = FORMATTER, level: int = LogLevel.DEBUG
) -> StreamHandler:
    handler = StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def make_file_handler(
    filepath: str,
    when: WhenType = "midnight",
    interval: int = 1,
    level: int = LogLevel.DEBUG,
    formatter: Formatter = FORMATTER,
    suffix: str = DEFAULT_SUFFIX,
) -> UTCTimedRotatingFileHandler:
    create_dir(os.path.dirname(filepath))
    handler = UTCTimedRotatingFileHandler(
        f"{filepath}{suffix}", when=when, interval=interval
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def init_file_logger(filepath: str) -> Logger:
    logger = get_logger()
    logger.addHandler(make_file_handler(filepath))
    return logger
