import logging
from logging.handlers import TimedRotatingFileHandler
from typing import NamedTuple

from ottopy.dt import utcfromtimestamp, strftime, utcnow
from ottopy.dt.formats import DtFormatStr


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


class UTCTimedRotatingFileHandler(TimedRotatingFileHandler):
    file_time_format = DtFormatStr.FILENAME_FORMAT

    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.pop("utc", True):
            raise ValueError(f"'utc' argument must be {True!r} or not set")

        TimedRotatingFileHandler.__init__(self, *args, **kwargs, utc=True)
        self.namer = self._namer

    def _namer(self, __):
        now = strftime(utcnow(), self.file_time_format)
        return f"{self.baseFilename}.{now}"


class _LogLevelType(NamedTuple):
    NOTSET: int = logging.NOTSET
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL


LogLevel = _LogLevelType()



