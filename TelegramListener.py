from telethon import TelegramClient, events

async def start_telegram_listener(callback, config):
    api_id = int(config["telegram_API_ID"])
    api_hash = config["telegram_API_hash"]
    target_chats = config["TARGET_CHATS"]

    client = TelegramClient('session_name', api_id, api_hash)

    @client.on(events.NewMessage(chats=target_chats))
    async def handler(event):
        sender = await event.get_sender()
        name = sender.username or sender.first_name or "Unknown" if sender else "Remedycore"
        text = event.raw_text
        chat = await event.get_chat()
        chat_name = getattr(chat, 'title', chat.username or str(chat.id))
        topic_id = getattr(event.message, 'thread_id', None)

        log_line = f"[{chat_name}] (Топик: {topic_id}) {name}: {text}"
        metadata = {
            "log_line": log_line,
            "chat_name": chat_name,
            "topic_id": topic_id,
            "sender": name
        }

        await callback(text, metadata)

    await client.start()
    print("🔌 Telegram подключён. Ждём сообщения...")
    await client.run_until_disconnected()