import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Type, Union, Tuple, TypeVar, Dict

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


@dataclass(frozen=True)
class CallResponse:
    payload: Any
    retries: int
    success: bool
    last_exception: Optional[Exception]
    exception: Optional[Exception] = field(default=None)


T = TypeVar("T")


def _fn_string(
    fn: Callable[..., T],
    validator: Callable[[T], T],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    all_fn_args = tuple(map(str, args)) + tuple(f"{k}={v}" for k, v in kwargs.items())
    all_args_str = ", ".join(all_fn_args)
    return f"{validator.__name__}({fn.__name__}({all_args_str}))"


def call_retry(
    fn: Callable[..., T],
    validator: Callable[[T], T],
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
        exception = RuntimeError(
            f"Failed {retries} times "
            f"calling {_fn_string(fn, validator, args, kwargs)}. "
            f"Last exception: {exc}"
        )
        return CallResponse(None, retries, False, exc, exception=exception)
