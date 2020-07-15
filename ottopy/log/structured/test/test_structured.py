from ottopy.dt import strptime_enum, DtFormatStr, UTC, DateTime
from ottopy.log.structured import timestamper, LOG_TS_KEY, parse_log_line
import mock


def test_timestamper() -> None:
    logger = mock.Mock()
    second = ""
    event_dict = {}
    timestamper(logger, second, event_dict)
    ts = event_dict.pop(LOG_TS_KEY)
    assert not event_dict
    # will fail if not parseable
    strptime_enum(ts, DtFormatStr.LOGGING_DATE_FORMAT)


def test_parse_log_line() -> None:
    line = '''
        {"_log_ts": "2020-04-01 15:43:21.123456Z", "event": "message", "payload": "hi"}
    '''.strip()
    (ts, event, body), error  = parse_log_line(line)
    assert ts == DateTime(2020, 4, 1, 15, 43, 21, 123456, tzinfo=UTC)
    assert event == "message"
    assert body == {"payload": "hi"}
    assert error is None


def test_parse_log_line_bad_json() -> None:
    line = "this is not json"
    data, error = parse_log_line(line)
    assert data is None
    assert isinstance(error, str)
