import asyncio
from openai import OpenAI
from src.telegram.TelegramListener import start_telegram_listener
from src.ai.MistralAI import analyze_message
from src.calendar.GCalendar import create_event_in_calendar, delete_handler_async
from src.telegram.TelegramNotification import notify_user, start_notification_server
from src.utils.configLoader import load_config

config = load_config()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config["mistralAI_key"],
)
BOT_TOKEN = config["telegram_notify_token"]
CHAT_ID = config["telegram_notify_chat_id"]

async def on_message_received(text: str, metadata: dict):
    print("📩 Новое сообщение:\n", metadata.get("log_line", text))

    result = analyze_message(text, client, config["context"])
    if result.get("has_event"):
        print("✅ Найдено событие:", result["event"])
        gcalendar_info = create_event_in_calendar(result["event"])
        notify_user(BOT_TOKEN, CHAT_ID, text, result["event"], gcalendar_info)
    else:
        print("ℹ️ Событий не обнаружено.")


async def main():
    print("🤖 Бот уведомитель запущен. Ожидаем новые сообщения...")
    print("🤖 Бот слушатель запущен. Ожидаем новые сообщения...")
    await asyncio.gather(
        start_notification_server(delete_handler_async),
        start_telegram_listener(on_message_received, config)
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())