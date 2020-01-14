import logging

from logging.handlers import TimedRotatingFileHandler

from ottopy.dt import DtFormatStr, utcfromtimestamp, strftime


class UTCMicroSecFormatter(logging.Formatter):
    default_time_format = DtFormatStr.LOGGING_DATE_FORMAT
    default_msec_format = None

    def converter(self, x):
        return utcfromtimestamp(x)

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            return strftime(ct, datefmt)
        else:
            return strftime(ct, self.default_time_format)


FORMATTER = UTCMicroSecFormatter(f"%(asctime)s %(name)s %(levelname)s >> %(message)s")


def get_logger(name: str = "", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def make_file_handler(
    filepath: str,
    when: str = "midnight",
    interval: int = 1,
    level=logging.DEBUG,
    formatter: logging.Formatter = FORMATTER,
    suffix: str = ".log",
) -> TimedRotatingFileHandler:
    handler = TimedRotatingFileHandler(
        f"{filepath}{suffix}", when=when, interval=interval, utc=True
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    return handler


def init_file_logger(filepath: str) -> logging.Logger:
    logger = get_logger()
    logger.addHandler(make_file_handler(filepath))
    return logger
