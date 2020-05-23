import json
import os
from typing import Tuple, Dict, Any, Optional, Union

from structlog import get_logger, configure, processors
from structlog._config import BoundLoggerLazyProxy as StructLogger

from ottopy.dt import DateTime, strftime, utcnow
from ottopy.dt.formats import DtFormatStr
from ottopy.log import Logger

__all__ = [
    "get_struct_logger",
    "parse_log_line",
    "ParsedLogLine",
    "StructLogger",
    "EventDict",
    "EVENT",
    "LOG_TS_KEY",
]

LOG_TS_KEY = "_log_ts"
EVENT = "event"

EventDict = Dict[str, Any]
ParsedLogLine = Tuple[DateTime, str, EventDict]
ParsedLogLineResult = Tuple[Optional[ParsedLogLine], Optional[str]]
StructLogger = StructLogger


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


def parse_log_line(line: Union[str, bytes]) -> ParsedLogLineResult:
    """Convert a struct logger line """
    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        return None, e.msg
    return (data.pop(LOG_TS_KEY), data.pop(EVENT), data), None


def log_startup_message(logger: StructLogger, name: str, git_rev: str) -> None:
    logger.msg(f"Started process", name=name, git_rev=git_rev, pid=os.getpid())
