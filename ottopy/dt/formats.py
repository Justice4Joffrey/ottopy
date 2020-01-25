from typing import NamedTuple


class _DtFormatStrType(NamedTuple):
    LOGGING_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f%z"
    FILENAME_FORMAT: str = "%Y-%m-%d.%H-%M-%S.%f%z"


DtFormatStr = _DtFormatStrType()