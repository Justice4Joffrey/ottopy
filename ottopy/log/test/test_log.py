import os
import tempfile
import unittest
from pathlib import Path

from ottopy.dt import DateTime, strptime
from ottopy.dt.formats import DtFormatStr
from ottopy.log import make_file_handler
from ottopy.log.consts import DEFAULT_SUFFIX


class TestLog(unittest.TestCase):
    def test_tr_handler_filename(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            base_filename = f"test"
            filename = f"{base_filename}{DEFAULT_SUFFIX}"
            filepath = os.path.join(d, base_filename)
            handler = make_file_handler(filepath)
            handler.doRollover()
            rolled = Path(tuple(x for x in os.listdir(d) if x != filename)[0])
            self.assertEqual(base_filename, rolled.stem.split(".")[0])
            self.assertEqual(2, len(rolled.suffixes))
            self.assertEqual(DEFAULT_SUFFIX, rolled.suffixes[1])
            self.assertEqual(".", rolled.suffixes[0][0])
            ext = rolled.suffixes[0][1:]
            dtime = strptime(ext, DtFormatStr.FILENAME_FORMAT)
            self.assertIsInstance(dtime, DateTime)
