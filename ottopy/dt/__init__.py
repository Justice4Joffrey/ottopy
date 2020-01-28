import datetime
from typing import Union

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


def new_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
    tzinfo: datetime.tzinfo = UTC,
    *,
    fold: int = 0,
) -> DateTime:
    if tzinfo is None:
        raise ValueError(f"tzinfo must not be {tzinfo!r}")
    return DateTime(
        year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo, fold=fold
    )


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
