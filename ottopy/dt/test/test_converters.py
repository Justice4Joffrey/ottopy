import unittest

from ottopy.dt.formats import parse_zulu_format, to_zulu_format


class TestConverters(unittest.TestCase):
    def test_parse_zulu_format(self) -> None:
        self.assertEqual("datetime_+0000", parse_zulu_format("datetime_Z"))

    def test_to_zulu_format(self) -> None:
        self.assertEqual("datetime_Z", to_zulu_format("datetime_+0000"))

    def test_to_zulu_format_raises(self) -> None:
        with self.assertRaises(ValueError):
            to_zulu_format("datetime_-0600")
