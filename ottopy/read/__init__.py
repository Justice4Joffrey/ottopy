import json
from typing import Dict, Any, Union


def read_file(filename: str, mode="rb") -> Union[str, bytes]:
    with open(filename, mode) as f:
        return f.read()


def read_json_file(filename: str) -> Dict[str, Any]:
    return parse_json(read_file(filename))


def parse_json(text: Union[str, bytes]) -> Dict[str, Any]:
    return json.loads(text)
