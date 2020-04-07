from requests import Session, Request, Response, PreparedRequest
from returns.io import impure_safe, IOResultE, IOResult
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import safe, ResultE


def send_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> ResultE[Response]:
    def _prepare(req: Request) -> ResultE[PreparedRequest]:
        return prepare(session, req)

    def _execute(prepared_request: PreparedRequest) -> IOResultE[Response]:
        return execute(session, prepared_request, allow_redirects=allow_redirects)

    return flow(request, _prepare, bind(_execute), IOResult.lift_result)


def send_json_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> ResultE[Response]:
    def _send_request(req: Request) -> ResultE[Response]:
        return send_request(session, req, allow_redirects=allow_redirects)

    return flow(request, _send_request, bind(validate_json), IOResult.lift_result)


@safe
def validate_json(response: Response) -> Response:
    response.json()
    return response


@impure_safe
def execute(
    session: Session, prepared_request: PreparedRequest, *, allow_redirects: bool = True
) -> Response:
    resp = session.send(prepared_request, allow_redirects=allow_redirects)
    resp.raise_for_status()
    return resp


@safe
def prepare(session: Session, request: Request) -> PreparedRequest:
    return session.prepare_request(request)
