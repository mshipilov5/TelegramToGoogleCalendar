import asyncio
from functools import partial
from openai import OpenAI
from TelegramListener import start_telegram_listener
from MistralAI import analyze_message
from GCalendar import create_event_in_calendar
from TelegramNotification import notify_user
from configLoader import load_config

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
        gcalendar_link = create_event_in_calendar(result["event"])
        notify_user(BOT_TOKEN, CHAT_ID, text, result["event"], gcalendar_link)
    else:
        print("ℹ️ Событий не обнаружено.")

async def main():
    print("🤖 Бот запущен. Ожидаем новые сообщения...")
    await start_telegram_listener(on_message_received, config)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())