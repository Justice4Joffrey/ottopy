from requests import Session, Request, Response, PreparedRequest
from returns.io import impure_safe, IOResultE
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import safe, ResultE


def send_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> IOResultE[Response]:
    def _lprepare(req: Request) -> ResultE[PreparedRequest]:
        return prepare(session, req)

    def _lexecute(prepared_request: PreparedRequest) -> IOResultE[Response]:
        return execute(session, prepared_request, allow_redirects=allow_redirects)

    return flow(request, _lprepare, bind(_lexecute))


def send_json_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> ResultE[Response]:
    def _lsend_request(req: Request) -> IOResultE[Response]:
        return send_request(session, req, allow_redirects=allow_redirects)

    return flow(request, _lsend_request, bind(validate_json))


def _validate_json(response: Response) -> Response:
    response.json()
    return response


def _execute(
    session: Session, prepared_request: PreparedRequest, *, allow_redirects: bool = True
) -> Response:
    resp = session.send(prepared_request, allow_redirects=allow_redirects)
    resp.raise_for_status()
    return resp


def _prepare(session: Session, request: Request) -> PreparedRequest:
    return session.prepare_request(request)


# the typing of decorators doesn't seem to work so great
validate_json = safe(_validate_json)
prepare = safe(_prepare)
execute = impure_safe(_execute)
