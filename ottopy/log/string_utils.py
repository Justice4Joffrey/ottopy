from typing import Tuple

from ottopy.dt import DateTime, strptime
from ottopy.dt.formats import DtFormatStr


def unicode_escape(string: str) -> str:
    return string.encode("unicode_escape").decode("utf-8")


def unicode_unescape(string: str) -> str:
    return string.encode("utf-8").decode("unicode_escape")


def parse_raw_line(line: str) -> Tuple[DateTime, str]:
    dt_str, msg = line.split(" >> ", 1)
    return strptime(dt_str, DtFormatStr.LOGGING_DATE_FORMAT), msg
