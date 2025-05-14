import datetime
import os.path
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.abspath("credentials/credentials.json")
print(f"Caminho absoluto das credenciais: {CREDENTIALS_PATH}")
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        all_events = []
        service = build("calendar", "v3", credentials=creds)
        not_wanted_calendars = [
            "Outros",
            "Feriados no Brasil",
            "Trabalho",
            "Faculdade"
        ]

        tz = pytz.timezone("America/Sao_Paulo")
        now = datetime.datetime.now(tz)
        start_of_day = now.replace(hour=0, minute=0, second=0).isoformat()
        end_of_day = now.replace(hour=23, minute=59, second=59).isoformat()
        all_calendars_infos = service.calendarList().list().execute().get("items", [])
        all_calendar_ids = [calendar for calendar in all_calendars_infos if calendar["summary"] not in not_wanted_calendars]
        print("Getting the upcoming 10 events")
        for calendar in all_calendar_ids:
            events_result = (
                service.events()
                .list(
                    calendarId=calendar["id"],
                    timeMin=start_of_day,
                    timeMax=end_of_day,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print(f"No upcoming events found in ID {calendar["summary"]}")
            else:
                for event in events:
                    all_events.append(event)

        # Prints the start and name of the next 10 events
        for event in all_events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()