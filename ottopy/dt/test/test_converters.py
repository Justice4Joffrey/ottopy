import pytest

from ottopy.dt import strftime, strftime_enum, strptime, strptime_enum, utcnow
from ottopy.dt.formats import DtFormatStr, parse_zulu_format, to_zulu_format


def test_parse_zulu_format() -> None:
    assert "datetime_+0000" == parse_zulu_format("datetime_Z")


def test_to_zulu_format() -> None:
    assert "datetime_Z" == to_zulu_format("datetime_+0000")


def test_to_zulu_format_raises() -> None:
    with pytest.raises(ValueError):
        to_zulu_format("datetime_-0600")


def test_strptime_enum() -> None:
    now = strftime(utcnow(), DtFormatStr.FILENAME_FORMAT.value)
    assert strptime_enum(now, DtFormatStr.FILENAME_FORMAT) == strptime(
        now, DtFormatStr.FILENAME_FORMAT.value
    )


def test_strftime_enum() -> None:
    now = utcnow()
    assert strftime_enum(now, DtFormatStr.FILENAME_FORMAT) == strftime(
        now, DtFormatStr.FILENAME_FORMAT.value
    )
