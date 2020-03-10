def unicode_escape(string: str) -> str:
    return string.encode("unicode_escape").decode("utf-8")


def unicode_unescape(string: str) -> str:
    return string.encode("utf-8").decode("unicode_escape")
