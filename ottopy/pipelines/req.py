import time
from typing import Any, Dict
from urllib.parse import urlparse

from requests import PreparedRequest, Request, Response, Session


class SuppressedSession(Session):
    def __init__(self, suppression_s: float):
        self.last_request_ts = 0.0
        self.suppression_s = suppression_s
        Session.__init__(self)

    def suppress(self) -> None:
        # TODO: you could parse the url, track the host and suppress only
        #  requests to the same site
        #  to make this useful you'll also have to clean up to
        time.sleep(max(0, self.last_request_ts + self.suppression_s - time.time()))

    def send(self, request: Request, **kwargs: Dict[str, Any]) -> Response:
        self.suppress()
        self.last_request_ts = time.time()
        return Session.send(self, request, **kwargs)


def send_request(
    session: Session,
    request: Request,
    *,
    allow_redirects: bool = True,
    raise_for_status: bool = True
) -> Response:
    prep = prepare(session, request)
    # Important! Host header directs routing for Traefik
    # I would prefer it read the URL, but I don't think it actually gets this as it's
    # handled in the DNS
    prep.headers["Host"] = urlparse(request.url).hostname
    resp = execute(
        session,
        prep,
        allow_redirects=allow_redirects,
        raise_for_status=raise_for_status,
    )
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
    session: Session,
    prepared_request: PreparedRequest,
    *,
    allow_redirects: bool = True,
    raise_for_status: bool = True
) -> Response:
    resp = session.send(prepared_request, allow_redirects=allow_redirects)
    if raise_for_status:
        resp.raise_for_status()
    return resp


def prepare(session: Session, request: Request) -> PreparedRequest:
    return session.prepare_request(request)
