import logging
from logging.handlers import TimedRotatingFileHandler
from typing import Any, Callable, Literal, NamedTuple, Optional

from ottopy.dt import DateTime, strftime, utcfromtimestamp, utcnow
from ottopy.dt.formats import DtFormatStr

WhenType = Literal[
    "s", "m", "h", "d", "w-1", "w1", "w2", "w3", "w4", "w5", "w6", "midnight"
]


class UTCMicroSecFormatter(logging.Formatter):
    default_time_format = DtFormatStr.LOGGING_DATE_FORMAT
    default_msec_format = ""

    def dt_converter(self, x: int) -> DateTime:
        return utcfromtimestamp(x)

    def formatTime(
        self, record: logging.LogRecord, datefmt: Optional[str] = None
    ) -> str:
        ct = self.dt_converter(record.created)
        if datefmt:
            return strftime(ct, datefmt)
        else:
            return strftime(ct, self.default_time_format)


class UTCTimedRotatingFileHandler(TimedRotatingFileHandler):
    file_time_format = DtFormatStr.FILENAME_FORMAT

    def __init__(
        self,
        filename: str,
        when: WhenType = "midnight",
        interval: int = 1,
        backupCount: int = 0,
        encoding: Optional[str] = None,
        delay: bool = False,
        atTime: Optional[DateTime] = None,
    ) -> None:
        TimedRotatingFileHandler.__init__(
            self,
            filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
            utc=True,
            atTime=atTime,
        )
        self.namer = self._namer

    def _namer(self, __: Any) -> str:
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
