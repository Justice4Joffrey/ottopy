import pytest

from ottopy.dt.formats import parse_zulu_format, to_zulu_format


def test_parse_zulu_format() -> None:
    assert "datetime_+0000" == parse_zulu_format("datetime_Z")


def test_to_zulu_format() -> None:
    assert "datetime_Z" == to_zulu_format("datetime_+0000")


def test_to_zulu_format_raises() -> None:
    with pytest.raises(ValueError):
        to_zulu_format("datetime_-0600")
