import re
from typing import cast

from ottopy.dt import datetime_from_regex, strftime, utcnow
from ottopy.dt.formats import DtFormatStr
from ottopy.dt.regexes import DtFormatStrRegex


def test_regexes() -> None:
    now = utcnow()
    now_sec = now.replace(microsecond=0)
    for field in DtFormatStr:
        pattern = getattr(DtFormatStrRegex, field.name).value
        date_str = strftime(now, field.value)
        match = re.match(pattern, date_str)
        match = cast(re.Match, match)
        assert match is not None
        parsed = datetime_from_regex(match)
        # allow seconds of deviation if ms not specified
        exp = now_sec if "%f" not in field.value else now
        assert (
            exp == parsed
        ), f"Field {field} format {field.value} doesn't match pattern {pattern}"
