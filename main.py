from telethon import TelegramClient, events
import asyncio

from GCalendar import create_event_in_calendar
from MistralAI import analyze_message
from configLoader import load_config

config = load_config()

api_id = int(config["telegram_API_ID"])
api_hash = config["telegram_API_hash"]
TARGET_CHATS = config["TARGET_CHATS"]

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=TARGET_CHATS))
async def handler(event):
    sender = await event.get_sender()
    if sender:
        name = sender.username or sender.first_name or "Unknown"
    else:
        name = "Remedycore"
    text = event.raw_text
    chat = await event.get_chat()
    chat_name = getattr(chat, 'title', chat.username or str(chat.id))
    topic_id = getattr(event.message, 'thread_id', None)

    log_line = f"[{chat_name}] (Топик: {topic_id}) {name}: {text}"
    print("📩 Новое сообщение:\n", log_line)

    result = analyze_message(text)
    if result.get("has_event"):
        print("✅ Найдено событие:", result["event"])
        create_event_in_calendar(result["event"])
    else:
        print("ℹ️ Событий не обнаружено.")

async def main():
    print("🤖 Бот запущен. Ожидаем новые сообщения...")
    await client.start()
    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())