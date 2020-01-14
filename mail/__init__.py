import base64
import os
import pickle
from email.mime.text import MIMEText
from typing import Dict, Any

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors

# noinspection PyProtectedMember
from googleapiclient.discovery import build, Resource

from mail import EmailBody, Email, EmailMeta, SendEmailResponse, InboxItems
from mail.classes import (
    EmailBody,
    EmailHeader,
    EmailPayload,
    Email,
    EmailMeta,
    SendEmailResponse,
    InboxItems,
)
from mail.config import SENDER, USER_ID, TOKEN_FILE, SCOPES


def email_from_dict(dct: Dict[str, Any]) -> Email:
    pl = dct["payload"]
    body = EmailBody(pl["body"]["size"], pl["body"]["data"])
    headers = tuple(EmailHeader(h["name"], h["value"]) for h in pl["headers"])
    payload = EmailPayload(pl["partId"], pl["mimeType"], pl["filename"], headers, body)
    return Email(
        dct["id"],
        dct["threadId"],
        dct["labelIds"],
        dct["snippet"],
        dct["historyId"],
        dct["internalDate"],
        payload,
        dct["sizeEstimate"],
    )


def inbox_items_from_dict(dct: Dict[str, Any]) -> InboxItems:
    messages = tuple(email_meta_from_dict(m) for m in dct["messages"])
    return InboxItems(messages, dct["nextPageToken"], dct["resultSizeEstimate"])


def email_meta_from_dict(dct: Dict[str, Any]) -> EmailMeta:
    return EmailMeta(dct["id"], dct["threadId"], dct.get("labelIds"))


def authenticate() -> Resource:
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(os.path.dirname(__file__), "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def send_email(
    service: Resource, message: Dict[str, str], user_id: str = USER_ID
) -> SendEmailResponse:
    """Send an email. For example:
    send_email(authenticate(), USER_ID, create_message(SENDER, SENDER, "Test", "this is a test."))

    :param service: Email session
    :param message: Text to send
    :param user_id: Session identifier (just set to 'me', nothing else works)
    :return: SendEmailResponse
    """
    try:
        meta = service.users().messages().send(userId=user_id, body=message).execute()
        return SendEmailResponse(email_meta=email_meta_from_dict(meta))
    except errors.HttpError as error:
        return SendEmailResponse(error=error)


def create_message(
    sender: str, to: str, subject: str, message_text: str
) -> Dict[str, str]:
    """Create message

    :param sender: From address
    :param to: To address (comma-separated string for multiple)
    :param subject: Subject
    :param message_text: Message
    :return: Dict with encoded message
    """
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    return {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}


def get_inbox(service: Resource, user_id: str = USER_ID) -> InboxItems:
    """Get inbox. Use get_email(service, message_id) with the "message_id" in "messages" to get
    an individual email.

    :param service: Email session
    :param user_id: Session identifier (just set to 'me', nothing else works)
    :return: InboxItems
    """
    return inbox_items_from_dict(
        service.users().messages().list(userId=user_id, labelIds=["INBOX"]).execute()
    )


def get_email(service: Resource, message_id: str, user_id: str = USER_ID) -> Email:
    """Get an email.

    :param service: Email session
    :param message_id: Unique message ID
    :param user_id: Session identifier (just set to 'me', nothing else works)
    :return: Email
    """
    return email_from_dict(
        service.users().messages().get(userId=user_id, id=message_id).execute()
    )
