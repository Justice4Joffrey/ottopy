import json
import os
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from structlog import BoundLogger, PrintLoggerFactory, configure, get_logger
from structlog import processors as _processors
from structlog import stdlib

from ottopy.dt import DateTime, new_nano_timestamp, utcfromnanotimestamp
from ottopy.log import Logger

__all__ = [
    "get_struct_logger",
    "parse_log_line",
    "stdlib",
    "timestamper",
    "LoggerFactory",
    "ParsedLogLine",
    "Processor",
    "StructLogger",
    "EventDict",
    "DEFAULT_PROCESSORS",
    "EVENT",
    "LOG_TS_KEY",
]

LOG_TS_KEY = "ts"
EVENT = "event"

EventDict = Dict[str, Any]
Processor = Callable[[Logger, str, EventDict], EventDict]
LoggerFactory = Union[PrintLoggerFactory, stdlib.LoggerFactory]
StructLogger = Type[BoundLogger]
stdlib = stdlib

ParsedLogLine = Tuple[DateTime, EventDict]
ParsedLogLineResult = Tuple[Optional[ParsedLogLine], Optional[str]]


def timestamper(_: Logger, __: str, event_dict: EventDict) -> EventDict:
    """Don't use structlog Timestamper as it's tz unaware"""
    event_dict[LOG_TS_KEY] = new_nano_timestamp()
    return event_dict


DEFAULT_PROCESSORS: Tuple[Processor, ...] = (
    timestamper,
    _processors.JSONRenderer(sort_keys=True, serializer=json.dumps),
)


def get_struct_logger(
    *logger_args: Any,
    processors: Tuple[Processor, ...] = DEFAULT_PROCESSORS,
    wrapper_class: Optional[StructLogger] = None,
    logger_factory: LoggerFactory = None,
) -> StructLogger:
    """Create a struct logger which creates each log line as a timestamped JSON"""
    configure(
        processors=list(processors),
        wrapper_class=wrapper_class,
        logger_factory=logger_factory,
    )
    return get_logger(*logger_args)


def parse_log_line(line: Union[str, bytes]) -> ParsedLogLineResult:
    """Convert a struct logger line """
    try:
        data = json.loads(line)
    except json.JSONDecodeError as e:
        return None, e.msg
    return (
        (utcfromnanotimestamp(data.pop(LOG_TS_KEY)), data,),
        None,
    )


def log_startup_message(logger: StructLogger, name: str, git_rev: str) -> None:
    logger.msg(f"Started process", name=name, git_rev=git_rev, pid=os.getpid())
