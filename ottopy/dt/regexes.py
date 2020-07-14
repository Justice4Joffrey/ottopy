import enum
import re

from ottopy.dt.formats import DtFormatStr

_TRANS = {
    "%Y": r"(\d{4})",
    "%m": r"(\d{2})",
    "%d": r"(\d{2})",
    "%H": r"(\d{2})",
    "%M": r"(\d{2})",
    "%S": r"(\d{2})",
    "%f": r"(\d{6})",
    "%z": r"([\+-]\d{4})",
}


def _substitute(string: str) -> str:
    for ph, sub in _TRANS.items():
        if ph in string:
            string = string.replace(ph, sub)
    if "%" in string:
        raise ValueError(f"Unsubstituted placeholder: {string!r}")
    return rf"{string}"


# mypy hates enums
# https://github.com/python/mypy/issues/5317
DtFormatStrRegex = enum.Enum(  # type: ignore
    "DtFormatStrRegex", {v.name: _substitute(re.escape(v.value)) for v in DtFormatStr}
)
