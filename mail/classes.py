from dataclasses import dataclass, field
from typing import Tuple, Optional


@dataclass(frozen=True)
class EmailBody:
    size: int
    data: str


@dataclass(frozen=True)
class EmailHeader:
    name: str
    value: str


@dataclass(frozen=True)
class EmailPayload:
    part_id: str
    mime_type: str
    filename: str
    headers: Tuple[EmailHeader, ...]
    body: EmailBody


@dataclass(frozen=True)
class Email:
    message_id: str
    thread_id: str
    label_ids: Tuple[str, ...]
    snippet: str
    history_id: str
    internal_date: str
    payload: EmailPayload
    size_estimate: int


@dataclass(frozen=True)
class EmailMeta:
    message_id: str
    thread_id: str
    label_ids: Optional[Tuple[str, ...]] = field(default=None)


@dataclass(frozen=True)
class SendEmailResponse:
    email_meta: Optional[EmailMeta] = field(default=None)
    error: Optional[Exception] = field(default=None)


@dataclass(frozen=True)
class InboxItems:
    messages: Tuple[EmailMeta, ...]
    next_page_token: str
    result_size_estimate: int
