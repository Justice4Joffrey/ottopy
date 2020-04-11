from typing import NamedTuple, Pattern

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
    return rf"^{string}$"


# mypy shits the bed with dynamic NamedTuples https://github.com/python/mypy/issues/848
_DtFormatStrRegex = NamedTuple(  # type: ignore
    "_DtFormatStrRegex", [(field, Pattern[str]) for field in DtFormatStr._fields]
)

DtFormatStrRegex = _DtFormatStrRegex(*[_substitute(s) for s in DtFormatStr])
