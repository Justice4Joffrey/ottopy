import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


@dataclass
class CallResponse:
    payload: Any
    retries: int
    last_exception: Optional[Exception]
    success: bool


def call_retry(
    fn: Callable,
    exceptions: ExceptionType,
    sleep: int,
    retries: int,
    *args: Tuple[Any],
    **kwargs: Dict[Any, Any]
) -> CallResponse:
    exc: Optional[Exception] = None
    for retry in range(retries):
        try:
            return CallResponse(fn(*args, **kwargs), retry, exc, True)
        except exceptions as e:
            exc = e
            time.sleep(sleep)
    else:
        return CallResponse(None, retries, exc, False)
