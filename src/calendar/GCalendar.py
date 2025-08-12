from exceptiongroup import catch
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
TOKEN_PATH = '../../token.json'

def create_event_in_calendar(event: dict):
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('../../client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

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
            "start": {
                "dateTime": start_datetime,
                "timeZone": "Europe/Moscow"
            },
            "end": {
                "dateTime": end_datetime,
                "timeZone": "Europe/Moscow"
            },
        }
    else:
        try:
            date_obj = datetime.fromisoformat(date)
            next_day = (date_obj + timedelta(days=1)).date().isoformat()
        except Exception as e:
            print("❌ Ошибка обработки даты:", e)
            return

        body = {
            "summary": title,
            "description": description,
            "start": {"date": date},
            "end": {"date": next_day},
        }

    try:
        event_result = service.events().insert(calendarId='primary', body=body).execute()
        return {
            "link": event_result.get('htmlLink'),
            "event_id": event_result.get('id')
        }
    except Exception as e:
        print("❌ Ошибка создания события в Google Calendar:", e)
        return



def delete_event_from_calendar(event_id: str) -> bool:
    try:
        creds = Credentials.from_authorized_user_file("../../token.json", ["https://www.googleapis.com/auth/calendar"])
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"🗑️ Событие {event_id} удалено.")
        return True  # Всё ок
    except HttpError as e:
        if e.resp.status == 410:
            print(f"⚠️ Событие {event_id} уже было удалено.")
            return False  # Уже удалено
        else:
            raise e

async def delete_handler_async(event_id: str) -> bool:
    return delete_event_from_calendar(event_id)

