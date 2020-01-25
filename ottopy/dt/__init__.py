from typing import NamedTuple, Union
import datetime

__all__ = [
    "DateTime",
    "DtFormatStr",
    "new_datetime",
    "strftime",
    "strptime",
    "utcnow",
    "utcfromtimestamp",
    "EPOCH",
    "UTC",
]

DateTime = datetime.datetime
_fromtimestamp = datetime.datetime.fromtimestamp
_strftime = datetime.datetime.strftime
_strptime = datetime.datetime.strptime
_now = datetime.datetime.now
UTC = datetime.timezone.utc


def new_datetime(*args, **kwargs) -> DateTime:
    return DateTime(*args, **kwargs, tzinfo=UTC)


EPOCH = new_datetime(1970, 1, 1, 0, 0, 0)


class _DtFormatStrType(NamedTuple):
    LOGGING_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f%z"
    FILENAME_FORMAT: str = "%Y-%m-%d.%H-%M-%S.%f%z"


DtFormatStr = _DtFormatStrType()


def utcfromtimestamp(ts: Union[float, int]) -> DateTime:
    return _fromtimestamp(ts, tz=UTC)


def strftime(dt: DateTime, fmt: str) -> str:
    return _strftime(dt, fmt)


def strptime(string: str, fmt: str) -> DateTime:
    return _strptime(string, fmt)


def utcnow() -> DateTime:
    return _now(tz=UTC)
