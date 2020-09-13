import datetime
import time
from typing import Match, Tuple, Union, cast

from ottopy.dt.formats import DtFormatStr

__all__ = [
    "DateTime",
    "Date",
    "Time",
    "new_datetime",
    "new_timestamp",
    "new_nano_timestamp",
    "datetime_from_regex",
    "strftime",
    "strptime",
    "strftime_enum",
    "strptime_enum",
    "timedelta",
    "DtFormatStr",
    "utcnow",
    "utcfromtimestamp",
    "utcfromnanotimestamp",
    "DISTANT_FUTURE",
    "EPOCH",
    "UTC",
]


DateTime = datetime.datetime
Date = datetime.date
Time = datetime.time
_fromtimestamp = datetime.datetime.fromtimestamp
_strftime = datetime.datetime.strftime
_strptime = datetime.datetime.strptime
_now = datetime.datetime.now
UTC = datetime.timezone.utc
NANOS = 1e9
timedelta = datetime.timedelta

DateTimeTuple = Union[
    Tuple[int, int, int],
    Tuple[int, int, int, int],
    Tuple[int, int, int, int, int],
    Tuple[int, int, int, int, int, int],
    Tuple[int, int, int, int, int, int, int],
]


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


def new_timestamp() -> float:
    return time.time()


def new_nano_timestamp() -> int:
    return int(time.time() * NANOS)


def datetime_from_regex(match: Match) -> DateTime:
    _tpl = tuple(map(int, match.groups()))
    if _tpl[-1] != 0:
        # don't bother handling non utc ts
        raise ValueError(f"Offset of {_tpl[-1]} not handled")
    tpl = cast(DateTimeTuple, _tpl[:-1])
    return new_datetime(*tpl)


DISTANT_FUTURE = new_datetime(9999, 12, 31, 23, 59, 59, 999999)
EPOCH = new_datetime(1970, 1, 1, 0, 0, 0)


def utcfromtimestamp(ts: Union[float, int]) -> DateTime:
    return _fromtimestamp(ts, tz=UTC)


def utcfromnanotimestamp(ts: Union[float, int]) -> DateTime:
    return utcfromtimestamp(ts / NANOS)


def strftime(dt: DateTime, fmt: str) -> str:
    return _strftime(dt, fmt)


def strptime(string: str, fmt: str) -> DateTime:
    return _strptime(string, fmt)


def strftime_enum(dt: DateTime, fmt: DtFormatStr) -> str:
    return _strftime(dt, fmt.value)


def strptime_enum(string: str, fmt: DtFormatStr) -> DateTime:
    return _strptime(string, fmt.value)


def utcnow() -> DateTime:
    return _now(tz=UTC)
