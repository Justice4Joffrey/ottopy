from typing import NamedTuple


class _DtFormatStrType(NamedTuple):
    LOGGING_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f%z"
    FILENAME_FORMAT: str = "%Y-%m-%d_%H-%M-%S_%f%z"
    FILENAME_FORMAT_SEC: str = "%Y-%m-%d_%H-%M-%S%z"


def parse_zulu_format(string: str) -> str:
    char = "Z"
    if not string.endswith(char):
        raise ValueError(f"String {string} must end with {char}")
    return string.replace(char, "+0000")


DtFormatStr = _DtFormatStrType()
