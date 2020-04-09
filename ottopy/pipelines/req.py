from requests import Session, Request, Response, PreparedRequest


def send_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> Response:
    prep = prepare(session, request)
    resp = execute(session, prep, allow_redirects=allow_redirects)
    return resp


def send_json_request(
    session: Session, request: Request, *, allow_redirects: bool = True
) -> Response:
    resp = send_request(session, request, allow_redirects=allow_redirects)
    validate_json(resp)
    return resp


def validate_json(response: Response) -> Response:
    response.json()
    return response


def execute(
    session: Session, prepared_request: PreparedRequest, *, allow_redirects: bool = True
) -> Response:
    resp = session.send(prepared_request, allow_redirects=allow_redirects)
    resp.raise_for_status()
    return resp


def prepare(session: Session, request: Request) -> PreparedRequest:
    return session.prepare_request(request)
