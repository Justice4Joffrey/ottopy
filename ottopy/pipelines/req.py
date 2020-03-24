from requests import Session, Request, Response, PreparedRequest
from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import safe, ResultE


def send_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> ResultE[Response]:
    return flow(
        request,
        lambda req: prepare(session, req),
        lambda prep_req: execute(session, prep_req, allow_redirects=allow_redirects),
    )


def send_json_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> ResultE[Response]:
    return flow(
        request,
        lambda req: send_request(session, req, allow_redirects=allow_redirects),
        bind(validate_json),
    )


@safe
def validate_json(response: Response) -> Response:
    response.json()
    return response


# @impure_safe
@safe
def execute(
    session: Session, prepared_request: PreparedRequest, *, allow_redirects: bool = True
) -> Response:
    resp = session.send(prepared_request, allow_redirects=allow_redirects)
    resp.raise_for_status()
    return resp


# @safe
def prepare(session: Session, request: Request) -> PreparedRequest:
    return session.prepare_request(request)
