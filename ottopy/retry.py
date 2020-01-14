import time
from dataclasses import dataclass
from typing import Callable, Union, Tuple, Any, Type

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


@dataclass
class CallResponse:
    payload: Any
    retries: int
    last_exception: ExceptionType
    success: bool


def call_retry(
    fn: Callable, exceptions: ExceptionType, sleep: int, retries: int, *args, **kwargs
) -> CallResponse:
    exc = None
    for retry in range(retries):
        try:
            return CallResponse(fn(*args, **kwargs), retry, exc, True)
        except exceptions as exc:
            time.sleep(sleep)
    else:
        return CallResponse(None, retries, exc, False)
