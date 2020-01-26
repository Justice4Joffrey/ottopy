import json
import os
from typing import Dict, Any, Union


HOME = os.path.expanduser("~")


def read_file(filename: str, *, mode: str = "rb") -> Union[str, bytes]:
    with open(filename, mode) as f:
        return f.read()


def read_json_file(filename: str, *, mode: str = "rb") -> Dict[str, Any]:
    return parse_json(read_file(filename, mode=mode))


def parse_json(text: Union[str, bytes]) -> Dict[str, Any]:
    return json.loads(text)
