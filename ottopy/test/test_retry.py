from unittest import mock

import pytest

from ottopy.retry import CallResponse, call_retry


def compare_response(expected: CallResponse, actual: CallResponse) -> None:
    assert actual.payload == expected.payload
    assert actual.retries == expected.retries
    assert actual.success == expected.success
    # comparison for exception
    if expected.last_exception is None or actual.last_exception is None:
        assert actual.last_exception == expected.last_exception
    else:
        assert isinstance(actual.last_exception, type(expected.last_exception))
        assert actual.last_exception.args == expected.last_exception.args
    if expected.exception is None or actual.exception is None:
        assert actual.exception == expected.exception
    else:
        assert isinstance(actual.exception, type(expected.exception))
        assert actual.exception.args == expected.exception.args


def test_call_retry_runs_out_of_attempts() -> None:
    fn = mock.Mock(
        side_effect=(
            KeyError("too bad"),
            KeyError("too bad"),
            KeyError("too bad"),
            123,
        )
    )
    fn.__name__ = "fn"
    actual = call_retry(fn, lambda x: x, KeyError, 0, 3, 1, 2, 3, a=5, b=8)
    expected = CallResponse(
        payload=None,
        retries=3,
        success=False,
        last_exception=KeyError("too bad"),
        exception=RuntimeError(
            "Failed 3 times calling <lambda>(fn(1, 2, 3, a=5, b=8)). "
            "Last exception: 'too bad'"
        ),
    )
    compare_response(expected, actual)


def test_call_retry_wrong_exc() -> None:
    with pytest.raises(ValueError):
        fn = mock.Mock(side_effect=ValueError("unhandled"))
        fn.__name__ = "fn"
        call_retry(fn, lambda x: x, KeyError, 0, 5, 1, 2, 3, a=5, b=8)


def test_call_retry_eventually_succeeds() -> None:
    fn = mock.Mock(
        side_effect=(
            KeyError("too bad"),
            KeyError("try again"),
            KeyError("once more"),
            123,
        )
    )
    fn.__name__ = "fn"
    actual = call_retry(fn, lambda x: x, KeyError, 0, 5, 1, 2, 3, a=5, b=8)
    expected = CallResponse(
        payload=123,
        retries=3,
        success=True,
        last_exception=KeyError("once more"),
        exception=None,
    )
    compare_response(expected, actual)
