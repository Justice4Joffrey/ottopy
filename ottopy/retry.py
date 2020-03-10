import time
from dataclasses import dataclass, field
from typing import (
    Any,
    Callable,
    Optional,
    Type,
    Union,
    Tuple,
    TypeVar,
    Dict,
    Generic,
    cast,
)

from requests import Response

ExceptionType = Union[Type[Exception], Tuple[Type[Exception], ...]]


T = TypeVar("T")


@dataclass(frozen=True)
class CallResponse(Generic[T]):
    payload: T
    retries: int
    success: bool
    last_exception: Optional[Exception]
    exception: Optional[Exception] = field(default=None)


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
    attempts: int,
    *args: Any,
    **kwargs: Any,
) -> CallResponse[Optional[T]]:
    exc: Optional[Exception] = None
    if attempts < 1:
        raise ValueError(f"Attempts must be 1 or greater, not {attempts}")
    for retry in range(attempts):
        try:
            return CallResponse(validator(fn(*args, **kwargs)), retry, True, exc)
        except exceptions as e:
            exc = e
            time.sleep(sleep)
    else:
        exception = RuntimeError(
            f"Failed {attempts} times "
            f"calling {_fn_string(fn, validator, args, kwargs)}. "
            f"Last exception: {exc}"
        )
        return CallResponse(None, attempts, False, exc, exception=exception)


def call_retry_or_raise(
    fn: Callable[..., T],
    validator: Callable[[T], T],
    exceptions: ExceptionType,
    sleep: int,
    attempts: int,
    *args: Any,
    **kwargs: Any,
) -> CallResponse[T]:
    resp = call_retry(fn, validator, exceptions, sleep, attempts, *args, **kwargs)
    if not resp.success:
        exc: Exception
        exc = cast(Exception, resp.exception)
        raise exc
    r: CallResponse[T]
    r = cast(CallResponse[T], resp)
    return r


def validate_response_200(response: Response) -> Response:
    if response.status_code != 200:
        raise ValueError(f"Status code {response.status_code}")
    else:
        return response
