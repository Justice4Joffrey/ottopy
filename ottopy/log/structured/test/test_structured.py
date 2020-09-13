from typing import cast

import mock

from ottopy.dt import new_datetime, timedelta, utcfromnanotimestamp, utcnow
from ottopy.log import Logger
from ottopy.log.structured import LOG_TS_KEY, EventDict, parse_log_line, timestamper


def test_timestamper() -> None:
    logger = mock.Mock()
    second = ""
    event_dict: EventDict = {}
    timestamper(cast(Logger, logger), second, event_dict)
    ts = event_dict.pop(LOG_TS_KEY)
    assert not event_dict
    # will fail if not parseable
    dt = utcfromnanotimestamp(ts)
    assert abs(utcnow() - dt) < timedelta(seconds=2)


def test_parse_log_line() -> None:
    line = """
        {"ts": 1599912431800779008, "event": "message", "payload": "hi"}
    """.strip()
    result, error = parse_log_line(line)
    assert result is not None
    ts, body = result
    assert ts == new_datetime(2020, 9, 12, 12, 7, 11, 800779)
    assert body == {"payload": "hi", "event": "message"}
    assert error is None


def test_parse_log_line_bad_json() -> None:
    line = "this is not json"
    data, error = parse_log_line(line)
    assert data is None
    assert isinstance(error, str)
