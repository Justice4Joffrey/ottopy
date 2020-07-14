from enum import Enum
from typing import Callable

UTC_OFFSET = "+0000"
ZULU = "Z"


# formats ending with _SEC will be expected to truncate microseconds in tests
class DtFormatStr(Enum):
    LOGGING_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"
    FILENAME_FORMAT = "%Y-%m-%d_%H-%M-%S_%f%z"
    FILENAME_FORMAT_SEC = "%Y-%m-%d_%H-%M-%S%z"


def _convert_suffix(from_str: str, to_str: str) -> Callable[[str], str]:
    def inner(string: str) -> str:
        if not string.endswith(from_str):
            raise ValueError(f"String {string} must end with {from_str}")
        return string.replace(from_str, to_str)

    return inner


parse_zulu_format = _convert_suffix(ZULU, UTC_OFFSET)
to_zulu_format = _convert_suffix(UTC_OFFSET, ZULU)
