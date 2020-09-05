import logging
import os.path
import pickle
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import Dict, List, Optional

# If modifying these scopes, delete the file token.pickle.
SCOPES: List[str] = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def build_service_spreadsheet() -> build:
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

    serv = build("sheets", "v4", credentials=creds, cache_discovery=False)
    return serv


def create_sheet_template() -> Optional[Dict[str, str]]:
    try:
        service: build = build_service_spreadsheet()
    except Exception as e:
        logging.error(f'Can not make service for sheets {e}', exc_info=True)
        return None

    try:
        if not os.path.exists("google_api/sprsh_link.txt"):
            with open("google_api/sprsh_link.txt", "w") as file:
                file.write(f"Spreadsheet id | Sheet name | Spreadsheet_link\n\n")
        spreadsheet = (
            service.spreadsheets().create(
                body={
                    "properties": {
                        "title": "Telegram_bot_applicatons",
                        "locale": "ru_RU",
                    },
                    "sheets": [
                        {
                            "properties": {
                                "sheetType": "GRID",
                                "sheetId": 0,
                                "title": "bot_appl",
                            }
                        }
                    ],
                }
            ).execute()
        )

        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet["spreadsheetId"],
            valueInputOption="USER_ENTERED",
            range=spreadsheet["sheets"][0]["properties"]["title"],
            insertDataOption="INSERT_ROWS",
            body={
                "values": [
                    [
                        "Telegram_id",
                        "Имя пользователя",
                        "Телефон",
                        "email",
                        "Желаемый курс",
                        "Время создания заявки",
                    ]
                ],
            },
        ).execute()

        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet["spreadsheetId"],
            body={
                "requests": [
                    {
                        "repeatCell": {
                            "cell": {
                                "userEnteredFormat": {
                                    "horizontalAlignment": "CENTER",
                                    "textFormat": {"fontSize": 12},
                                }
                            },
                            "range": {
                                "sheetId": 0,
                                "startRowIndex": 0,
                                "endRowIndex": 1,
                                "startColumnIndex": 0,
                                "endColumnIndex": 6,
                            },
                            "fields": "userEnteredFormat",
                        }
                    },
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                                "endIndex": 1,
                            },
                            "properties": {"pixelSize": 140},
                            "fields": "pixelSize",
                        }
                    },
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 1,
                                "endIndex": 3,
                            },
                            "properties": {"pixelSize": 170},
                            "fields": "pixelSize",
                        }
                    },
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 3,
                                "endIndex": 5,
                            },
                            "properties": {"pixelSize": 200},
                            "fields": "pixelSize",
                        }
                    },
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": 0,
                                "dimension": "COLUMNS",
                                "startIndex": 5,
                                "endIndex": 6,
                            },
                            "properties": {"pixelSize": 250},
                            "fields": "pixelSize",
                        }
                    },
                ]
            },
        ).execute()

        with open("google_api/sprsh_link.txt", "a") as file:
            file.write(
                f'{spreadsheet["spreadsheetId"]} | '
                f'{spreadsheet["sheets"][0]["properties"]["title"]} | '
                f'{spreadsheet["spreadsheetUrl"]}\n'
            )
        logging.info('Successfully created spreadsheet')
        return {
            "spreadsheet_id": spreadsheet["spreadsheetId"],
            "sheet_name": spreadsheet["sheets"][0]["properties"]["title"],
        }
    except HttpError as e:
        logging.error(f'Can not make sheet template {e}', exc_info=True)
        return None


def add_data_to_sprsh(
        user: Dict[str, str], spreadsheet: Optional[Dict[str, str]]) -> bool:
    try:
        service: build = build_service_spreadsheet()
    except Exception as e:
        logging.error(f'Can not make service for sheets {e}', exc_info=True)
        return False
    try:
        service.spreadsheets().values().append(
                spreadsheetId=spreadsheet["spreadsheet_id"],
                valueInputOption="USER_ENTERED",
                range=spreadsheet["sheet_name"],
                insertDataOption="INSERT_ROWS",
                body={
                    "values": [[item for item in user.values()]],
                },
        ).execute()
        logging.info('Successfully added data to spreadsheet')
        return True
    except HttpError as e:
        logging.error(f'Can not add data to sheet {e}', exc_info=True)
        return False
