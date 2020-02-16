import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Type, Union, Tuple

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


@dataclass(frozen=True)
class CallResponse:
    payload: Any
    retries: int
    success: bool
    last_exception: Optional[Exception]
    exception: Optional[Exception] = field(default=None)


def call_retry(
    fn: Callable,
    validator: Callable,
    exceptions: ExceptionType,
    sleep: int,
    retries: int,
    *args: Any,
    **kwargs: Any,
) -> CallResponse:
    exc: Optional[Exception] = None
    for retry in range(retries):
        try:
            return CallResponse(validator(fn(*args, **kwargs)), retry, True, exc)
        except exceptions as e:
            exc = e
            time.sleep(sleep)
    else:
        all_fn_args = args + tuple(f"{k}={v}" for k, v in kwargs.items())
        all_args_str = ", ".join(all_fn_args)
        fn_str = f"{fn.__name__}({all_args_str})"
        exception = RuntimeError(
            f"Failed {retries} times calling {fn_str}. Last exception: {exc}"
        )
        return CallResponse(None, retries, False, exc, exception=exception)
