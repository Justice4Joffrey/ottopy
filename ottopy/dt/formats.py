from typing import Callable, NamedTuple

UTC_OFFSET = "+0000"
ZULU = "Z"


class _DtFormatStrType(NamedTuple):
    LOGGING_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f%z"
    FILENAME_FORMAT: str = "%Y-%m-%d_%H-%M-%S_%f%z"
    FILENAME_FORMAT_SEC: str = "%Y-%m-%d_%H-%M-%S%z"


def _convert_suffix(from_str: str, to_str: str) -> Callable[[str], str]:
    def inner(string: str) -> str:
        if not string.endswith(from_str):
            raise ValueError(f"String {string} must end with {from_str}")
        return string.replace(from_str, to_str)

    return inner


parse_zulu_format = _convert_suffix(ZULU, UTC_OFFSET)
to_zulu_format = _convert_suffix(UTC_OFFSET, ZULU)


DtFormatStr = _DtFormatStrType()
