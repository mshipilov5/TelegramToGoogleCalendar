from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# Если вы редактируете календарь, нужна эта область
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event_in_calendar(event: dict):
    creds = None
    if creds is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES
        )
        creds = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=creds)

    title = event.get("title")
    date = event.get("date")
    time = event.get("time")
    description = event.get("description", "")

    if time:
        # Событие со временем (datetime-local)
        start_datetime = f"{date}T{time}:00"
        end_datetime = f"{date}T{time}:00"

        body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_datetime, "timeZone": "Europe/Moscow"},
            "end": {"dateTime": end_datetime, "timeZone": "Europe/Moscow"},
        }
    else:
        # Событие без времени (all-day)
        body = {
            "summary": title,
            "description": description,
            "start": {"date": date},
            "end": {"date": date},
        }

    event = service.events().insert(calendarId='primary', body=body).execute()
    print(f"✅ Событие создано: {event.get('htmlLink')}")