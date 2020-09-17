import base64
import logging
import pickle
import os.path
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import Dict, List


# If modifying these scopes, delete the file token.pickle.
SCOPES: List[str] = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

EMAIL_RECEIVER: str = "maksimvoznyuk@gmail.com"


def build_service_gmail() -> build:
    creds: build.credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("google_api/token.pickle"):
        with open("google_api/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_api/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("google_api/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    serv = build("gmail", "v1", credentials=creds, cache_discovery=False)

    return serv


def create_message(
        sender: str, to: str, subject: str, message_text: str
) -> Dict[str, str]:
    message: MIMEText = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        "raw": raw_message.decode("utf-8")
    }


def send_email(subject: str, _message: str) -> bool:
    try:
        service = build_service_gmail()
    except Exception as e:
        logging.error(f'Can not make service for gmail{e}', exc_info=True)
        return False
    message = create_message(
        "me", EMAIL_RECEIVER, f"{subject}", f"{_message}"
    )
    try:
        service.users().messages().send(
            userId="me", body=message
        ).execute()
        logging.info('email sent successfully')
        return True
    except HttpError as error:
        logging.error(f'Cannot send email {error}', exc_info=True)
        return False
