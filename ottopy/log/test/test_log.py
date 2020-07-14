import os
from pathlib import Path, PosixPath

from ottopy.dt import DateTime, strptime
from ottopy.dt.formats import DtFormatStr
from ottopy.log import make_file_handler
from ottopy.log.consts import DEFAULT_SUFFIX


def test_tr_handler_filename(tmp_path: PosixPath) -> None:
    base_filename = f"test"
    filename = f"{base_filename}{DEFAULT_SUFFIX}"
    filepath = os.path.join(tmp_path, base_filename)
    handler = make_file_handler(filepath)
    handler.doRollover()
    rolled = Path(tuple(x for x in os.listdir(str(tmp_path)) if x != filename)[0])
    assert rolled.stem.split(".")[0] == base_filename
    assert len(rolled.suffixes) == 2
    assert rolled.suffixes[1] == DEFAULT_SUFFIX
    assert rolled.suffixes[0][0] == "."
    ext = rolled.suffixes[0][1:]
    dtime = strptime(ext, DtFormatStr.FILENAME_FORMAT.value)
    assert isinstance(dtime, DateTime)
