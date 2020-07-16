from dataclasses import dataclass
from typing import Optional

from requests import Request, RequestException, Response, Session

from ottopy.pipelines.req import send_request


@dataclass(frozen=True)
class WrappedResponse:
    response: Optional[Response]
    success: bool = True
    connection_error: bool = False


def send_request_no_exc(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> WrappedResponse:
    try:
        response = send_request(
            session, request, allow_redirects=allow_redirects, raise_for_status=False
        )
    except RequestException:
        return WrappedResponse(None, success=False, connection_error=True)
    return WrappedResponse(response, success=400 <= response.status_code < 600)
