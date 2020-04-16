import json
from typing import Tuple, Dict, Any

from structlog import get_logger, configure, processors
from structlog._config import BoundLoggerLazyProxy

from ottopy.dt import DateTime
from ottopy.dt.formats import DtFormatStr

LOG_TS_KEY = "_log_ts"
EVENT = "event"


def get_struct_logger() -> BoundLoggerLazyProxy:
    """Create a struct logger which creates each log line as a timestamped JSON"""
    configure(
        processors=[
            processors.TimeStamper(fmt=DtFormatStr.LOGGING_DATE_FORMAT, key=LOG_TS_KEY),
            processors.JSONRenderer(sort_keys=True, serializer=json.dumps),
        ],
    )
    return get_logger()


def parse_log_line(line: str) -> Tuple[DateTime, str, Dict[str, Any]]:
    """Convert a struct logger line """
    data = json.loads(line)
    return data.pop(LOG_TS_KEY), data.pop(EVENT), data
