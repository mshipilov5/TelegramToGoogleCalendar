import json
from datetime import datetime
from openai import OpenAI
from configLoader import load_config

config = load_config()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config["mistralAI_key"],
)

weekday_ru = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье',
}

def analyze_message(text: str) -> dict:
    now = datetime.now()
    date_str = f"сегодня {now.day} {now.strftime('%B')} {now.year} года, {now.strftime('%H:%M')} {weekday_ru[now.weekday()]}"

    prompt = f"""
Анализируй текст ниже и определи, есть ли в нём информация о событии, которое нужно добавить в Google Calendar (например: встречи, дедлайны, напоминания).
{date_str}
**Критерии события:**
- Дата (обязательно)
- Время (желательно)
- Название/описание события (обязательно)

Если событие найдено, выведи ТОЛЬКО ответ в формате JSON БЕЗ КАВЫЧЕК И УКАЗАНИЯ ЧТО ЭТО JSON 
СООБЩЕНИЕ ОБЯЗАНО НАЧИНАТЬСЯ С ФИГУРНОЙ СКОБКИ:

{{
  "has_event": true,
  "event": {{
    "title": "Название события",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "description": "Доп. информация"
  }}
}}

Если события нет, верни ТОЛЬКО и ничего кроме json:
{{
  "has_event": false,
  "event": null
}}

Текст: {text}
"""

    response = client.chat.completions.create(
        model="mistralai/devstral-small:free",
        messages=[{"role": "user", "content": prompt}]
    )

    message = response.choices[0].message.content.strip()

    try:
        result = json.loads(message)
        return result
    except Exception as e:
        print("❌ Ошибка парсинга ответа от ИИ:", e)
        print("Ответ был:", message)
        return {"has_event": False, "event": None}
