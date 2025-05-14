import datetime
import os
import pytz
import logging


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from services.twilio import TwilioService

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.abspath("credentials/credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
NOT_WANTED_CALENDARS = ["Outros", "Feriados no Brasil", "Trabalho", "Faculdade"]

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def authenticate():
    """Autentica o usuário e retorna as credenciais."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
    return creds


def get_calendar_service(creds):
    """Cria o serviço do Google Calendar."""
    return build("calendar", "v3", credentials=creds)


def get_events(service, calendar_id, start_of_day, end_of_day):
    """Obtém eventos de um calendário específico."""
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_of_day,
            timeMax=end_of_day,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        return events_result.get("items", [])
    except HttpError as error:
        logging.error(f"Erro ao obter eventos do calendário {calendar_id}: {error}")
        return []


def main():
    creds = authenticate()
    service = get_calendar_service(creds)

    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.datetime.now(tz)
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat()

    twilio_service = TwilioService()

    try:
        all_calendars = service.calendarList().list().execute().get("items", [])
        filtered_calendars = [
            calendar for calendar in all_calendars if calendar["summary"] not in NOT_WANTED_CALENDARS
        ]

        all_events = []
        for calendar in filtered_calendars:
            events = get_events(service, calendar["id"], start_of_day, end_of_day)
            if not events:
                logging.info(f"Sem eventos no calendário: {calendar['summary']}")
            else:
                all_events.extend(events)

        if all_events:
            message_body = "🗓️ Seus eventos de hoje:\n\n"
            for event in all_events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                message_body += f"• {start} - {event['summary']}\n"
        else:
            message_body = "Você não tem eventos agendados para hoje! ✅"

        # Envia a mensagem para o WhatsApp
        twilio_service.send_message(message_body)

    except HttpError as error:
        logging.error(f"Ocorreu um erro: {error}")


if __name__ == "__main__":
    main()
