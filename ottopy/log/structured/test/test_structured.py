import mock

from ottopy.dt import UTC, DateTime, DtFormatStr, strptime_enum
from ottopy.log.structured import LOG_TS_KEY, EventDict, parse_log_line, timestamper


def test_timestamper() -> None:
    logger = mock.Mock()
    second = ""
    event_dict: EventDict = {}
    timestamper(logger, second, event_dict)
    ts = event_dict.pop(LOG_TS_KEY)
    assert not event_dict
    # will fail if not parseable
    strptime_enum(ts, DtFormatStr.LOGGING_DATE_FORMAT)


def test_parse_log_line() -> None:
    line = """
        {"_log_ts": "2020-04-01 15:43:21.123456Z", "event": "message", "payload": "hi"}
    """.strip()
    result, error = parse_log_line(line)
    assert result is not None
    ts, body = result
    assert ts == DateTime(2020, 4, 1, 15, 43, 21, 123456, tzinfo=UTC)
    assert body == {"payload": "hi", "event": "message"}
    assert error is None


def test_parse_log_line_bad_json() -> None:
    line = "this is not json"
    data, error = parse_log_line(line)
    assert data is None
    assert isinstance(error, str)
