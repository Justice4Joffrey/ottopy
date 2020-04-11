import re
import unittest
from typing import cast

from ottopy.dt import utcnow, strftime, datetime_from_regex
from ottopy.dt.formats import DtFormatStr
from ottopy.dt.regexes import DtFormatStrRegex


class TestRegexes(unittest.TestCase):
    def test_regexes(self) -> None:
        now = utcnow()
        for field in DtFormatStr._fields:
            fmt = getattr(DtFormatStr, field)
            pattern = getattr(DtFormatStrRegex, field)
            date_str = strftime(now, fmt)
            match = re.match(pattern, date_str)
            match = cast(re.Match, match)
            self.assertIsNotNone(match)
            parsed = datetime_from_regex(match)
            self.assertEqual(
                now,
                parsed,
                f"Field {field} format {fmt} doesn't match pattern {pattern}",
            )
