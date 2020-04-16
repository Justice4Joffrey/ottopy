import json
from typing import Tuple, Dict, Any

from structlog import get_logger, configure, processors
from structlog._config import BoundLoggerLazyProxy as StructLogger

from ottopy.dt import DateTime, strftime, utcnow
from ottopy.dt.formats import DtFormatStr
from ottopy.log import Logger

__all__ = [
    "get_struct_logger",
    "parse_log_line",
    "StructLogger",
    "EventDict",
    "EVENT",
    "LOG_TS_KEY",
]

LOG_TS_KEY = "_log_ts"
EVENT = "event"

EventDict = Dict[str, Any]


def timestamper(_: Logger, __: str, event_dict: EventDict) -> EventDict:
    """Don't use structlog Timestamper as it's tz unaware"""
    event_dict[LOG_TS_KEY] = strftime(utcnow(), DtFormatStr.LOGGING_DATE_FORMAT)
    return event_dict


def get_struct_logger() -> StructLogger:
    """Create a struct logger which creates each log line as a timestamped JSON"""
    configure(
        processors=[
            timestamper,
            processors.JSONRenderer(sort_keys=True, serializer=json.dumps),
        ],
    )
    return get_logger()


def parse_log_line(line: str) -> Tuple[DateTime, str, Dict[str, Any]]:
    """Convert a struct logger line """
    data = json.loads(line)
    return data.pop(LOG_TS_KEY), data.pop(EVENT), data
