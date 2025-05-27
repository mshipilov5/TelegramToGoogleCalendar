import json
from datetime import datetime

weekday_ru = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'суббота',
    6: 'воскресенье',
}

def load_prompt_template():
    with open("prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

PROMPT_TEMPLATE = load_prompt_template()

def analyze_message(text: str, client) -> dict:
    now = datetime.now()
    date_str = f"сегодня {now.day} {now.strftime('%B')} {now.year} года, {now.strftime('%H:%M')} {weekday_ru[now.weekday()]}"
    prompt = PROMPT_TEMPLATE.format(date_str=date_str, text=text)

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