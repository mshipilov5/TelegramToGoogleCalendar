import requests

def notify_user(bot_token: str, chat_id: str, message: str, parsed_event: dict, link: str) -> None:
    link = next(iter(link)) if isinstance(link, set) else link

    event_text = "\n".join(f"<b>{key.capitalize()}:</b> {value}" for key, value in parsed_event.items())

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"{message}\n\n{event_text}\n\n🔗 <a href=\"{link}\">Открыть в Google Календаре</a>",
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("⚠️ Ошибка при отправке уведомления в Telegram:", e)