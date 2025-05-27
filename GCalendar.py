from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

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
        try:
            if "-" in time:
                start_str, end_str = time.split("-")
                start_datetime = f"{date}T{start_str}:00"
                end_datetime = f"{date}T{end_str}:00"
            else:
                # Одно время: "10:00"
                start = datetime.fromisoformat(f"{date}T{time}")
                end = start + timedelta(hours=1)
                start_datetime = start.isoformat()
                end_datetime = end.isoformat()
        except Exception as e:
            print("❌ Ошибка обработки времени:", e)
            return

        body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_datetime, "timeZone": "Europe/Moscow"},
            "end": {"dateTime": end_datetime, "timeZone": "Europe/Moscow"},
        }
    else:
        body = {
            "summary": title,
            "description": description,
            "start": {"date": date},
            "end": {"date": (datetime.fromisoformat(date) + timedelta(days=1)).date().isoformat()},
        }

    event = service.events().insert(calendarId='primary', body=body).execute()
    return {event.get('htmlLink')}