from typing import List, Sequence

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_service(credentials_path: str = "credentials.json"):
    """
    Creates an authenticated Google Sheets API client using a service account.
    """
    creds = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES,
    )
    service = build("sheets", "v4", credentials=creds)
    return service


def append_rows(
    spreadsheet_id: str,
    range_name: str,
    rows: List[Sequence],
):
    """
    Appends rows to a Google Sheet.

    rows: list of lists, each inner list is one row.
    The order of columns must match your sheet:
      Title, Job Description, Platform, Link, Date, Rating,
      Posting Date, Job Type, Company Name, Company Description,
      Skills, Resume Match, Cover Letter, Salary, City,
      Expired, Remote, Salary.1, Status
    """
    service = get_sheets_service()
    body = {"values": rows}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        )
        .execute()
    )

    return result
