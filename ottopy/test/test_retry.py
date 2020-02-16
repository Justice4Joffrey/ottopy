import unittest
from unittest import mock

from ottopy.retry import call_retry, CallResponse


class TestRetry(unittest.TestCase):
    def compare_response(self, expected: CallResponse, actual: CallResponse) -> None:
        self.assertEqual(expected.payload, actual.payload)
        self.assertEqual(expected.retries, actual.retries)
        self.assertEqual(expected.success, actual.success)
        # comparison for exception
        if expected.last_exception is None or actual.last_exception is None:
            self.assertEqual(expected.last_exception, actual.last_exception)
        else:
            self.assertEqual(type(expected.last_exception), type(actual.last_exception))
            self.assertEqual(expected.last_exception.args, actual.last_exception.args)
        if expected.exception is None or actual.exception is None:
            self.assertEqual(expected.exception, actual.exception)
        else:
            self.assertEqual(type(expected.exception), type(actual.exception))
            self.assertEqual(expected.exception.args, actual.exception.args)

    def test_call_retry_runs_out_of_attempts(self) -> None:
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
        self.compare_response(expected, actual)

    def test_call_retry_wrong_exc(self) -> None:
        with self.assertRaises(ValueError):
            fn = mock.Mock(side_effect=ValueError("unhandled"))
            fn.__name__ = "fn"
            call_retry(fn, lambda x: x, KeyError, 0, 5, 1, 2, 3, a=5, b=8)

    def test_call_retry_eventually_succeeds(self) -> None:
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
        self.compare_response(expected, actual)
