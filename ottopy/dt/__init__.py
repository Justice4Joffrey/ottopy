from typing import Union
import datetime

__all__ = [
    "DateTime",
    "new_datetime",
    "strftime",
    "strptime",
    "utcnow",
    "utcfromtimestamp",
    "DISTANT_FUTURE",
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


DISTANT_FUTURE = new_datetime(9999, 12, 31, 23, 59, 59, 999999)
EPOCH = new_datetime(1970, 1, 1, 0, 0, 0)


def utcfromtimestamp(ts: Union[float, int]) -> DateTime:
    return _fromtimestamp(ts, tz=UTC)


def strftime(dt: DateTime, fmt: str) -> str:
    return _strftime(dt, fmt)


def strptime(string: str, fmt: str) -> DateTime:
    return _strptime(string, fmt)


def utcnow() -> DateTime:
    return _now(tz=UTC)
