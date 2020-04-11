import datetime
from typing import Union, Match, cast, Tuple

__all__ = [
    "DateTime",
    "Date",
    "Time",
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
Date = datetime.date
Time = datetime.time
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


def datetime_from_regex(match: Match) -> DateTime:
    tpl = tuple(map(int, match.groups()))
    if len(tpl) == 8:
        if tpl[-1] != 0:
            # don't bother handling non utc ts
            raise ValueError(f"Offset of {tpl[-1]} not handled")
        tpl = tpl[:-1]
    if len(tpl) != 7:
        raise TypeError(f"Cannot handle tuple length {len(tpl)} - {tpl}")
    tpl = cast(Tuple[int, int, int, int, int, int, int], tpl)
    return new_datetime(*tpl)


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
