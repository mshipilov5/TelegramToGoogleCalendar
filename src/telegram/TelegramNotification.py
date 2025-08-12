import asyncio
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
from uvicorn import Config, Server

app = FastAPI()
BOT_TOKEN = None
DELETE_HANDLER: Callable[[str], Awaitable[None]] = None


def notify_user(bot_token: str, chat_id: str, message: str, parsed_event: dict, event_info: dict) -> None:
    global BOT_TOKEN
    BOT_TOKEN = bot_token

    link = event_info.get("link")
    event_id = event_info.get("event_id")

    event_text = "\n".join(
        f"<b>{key.capitalize()}:</b> {value}" for key, value in parsed_event.items()
    )

    keyboard = {
        "inline_keyboard": [[
            {
                "text": "❌ Отменить событие",
                "callback_data": f"cancel_event:{event_id}"
            }
        ]]
    }

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"{message}\n\n{event_text}\n\n🔗 <a href=\"{link}\">Открыть в Google Календаре</a>",
        "parse_mode": "HTML",
        "reply_markup": keyboard
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("⚠️ Ошибка при отправке уведомления в Telegram:", e)


@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()

    if "callback_query" in data:
        query = data["callback_query"]
        callback_data = query.get("data", "")
        chat_id = query["message"]["chat"]["id"]
        message_id = query["message"]["message_id"]

        if callback_data.startswith("cancel_event:"):
            event_id = callback_data.split(":", 1)[1]

            error_msg = None
            if DELETE_HANDLER:
                try:
                    success = await DELETE_HANDLER(event_id)
                    if not success:
                        error_msg = "⚠️ Событие уже было удалено ранее."
                except Exception as e:
                    error_msg = "⚠️ Не удалось отменить событие."
                    print("Ошибка при удалении события:", e)

            answer_url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
            requests.post(answer_url, json={
                "callback_query_id": query["id"],
                "text": "❌ Событие отменено." if not error_msg else error_msg,
                "show_alert": False
            })

            new_text = "❌ Событие отменено." if not error_msg else error_msg
            edit_url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
            requests.post(edit_url, json={
                "chat_id": chat_id,
                "message_id": message_id,
                "text": new_text,
            })

    return JSONResponse(content={"ok": True})


async def start_notification_server(delete_handler: Callable[[str], Awaitable[None]]):
    global DELETE_HANDLER
    DELETE_HANDLER = delete_handler

    print("🚀 FastAPI-сервер Telegram бота запущен на http://localhost:8000/webhook")

    config = Config(app=app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)

    await server.serve()