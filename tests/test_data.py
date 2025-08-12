TEST_CONFIG = {
    "info": {
        "mistralAI_key": "test_key_123456789",
        "telegram_API_ID": "12345",
        "telegram_API_hash": "test_hash_abcdef123456",
        "name": "TestBot",
        "TARGET_CHATS": ["chat1", "chat2", "chat3"],
        "telegram_notify_token": "bot_token_123456789",
        "telegram_notify_chat_id": "chat_id_123456789",
        "context": "рабочие встречи и события"
    }
}

TEST_MESSAGES = [
    "Встреча завтра в 15:00",
    "Событие 25 декабря в 10:00",
    "Встреча с клиентом в понедельник в 14:30",
    "Презентация проекта в пятницу",
    "Совещание команды каждый вторник в 9:00",
    "Встреча с партнерами 30 января в 16:00-17:30",
    "Конференция 15 марта весь день",
    "Встреча по проекту завтра с 13:00 до 15:00",
    "Планирование на следующую неделю",
    "Ревью кода в четверг в 11:00"
]

TEST_EVENTS = [
    {
        "title": "Встреча с клиентом",
        "date": "2024-01-15",
        "time": "15:00-16:00",
        "description": "Обсуждение проекта"
    },
    {
        "title": "Совещание команды",
        "date": "2024-01-16",
        "time": "9:00",
        "description": "Еженедельное планирование"
    },
    {
        "title": "Презентация",
        "date": "2024-01-17",
        "time": "14:00-15:30",
        "description": "Демонстрация результатов"
    },
    {
        "title": "Конференция",
        "date": "2024-01-18",
        "description": "Международная конференция по ИИ"
    },
    {
        "title": "Ревью кода",
        "date": "2024-01-19",
        "time": "11:00",
        "description": "Код-ревью проекта"
    }
]

TEST_METADATA = [
    {
        "log_line": "[Рабочий чат] (Топик: 123) Иван: Встреча завтра в 15:00",
        "chat_name": "Рабочий чат",
        "topic_id": 123,
        "sender": "Иван"
    },
    {
        "log_line": "[Проект А] Мария: Событие 25 декабря в 10:00",
        "chat_name": "Проект А",
        "topic_id": None,
        "sender": "Мария"
    },
    {
        "log_line": "[Команда разработки] Алексей: Встреча с клиентом в понедельник в 14:30",
        "chat_name": "Команда разработки",
        "topic_id": 456,
        "sender": "Алексей"
    },
    {
        "log_line": "[Менеджмент] Елена: Презентация проекта в пятницу",
        "chat_name": "Менеджмент",
        "topic_id": None,
        "sender": "Елена"
    },
    {
        "log_line": "[Общий чат] Петр: Совещание команды каждый вторник в 9:00",
        "chat_name": "Общий чат",
        "topic_id": None,
        "sender": "Петр"
    }
]

TEST_AI_RESPONSES = [
    {
        "has_event": True,
        "event": {
            "title": "Встреча с клиентом",
            "date": "2024-01-15",
            "time": "15:00-16:00",
            "description": "Обсуждение проекта"
        }
    },
    {
        "has_event": True,
        "event": {
            "title": "Совещание команды",
            "date": "2024-01-16",
            "time": "9:00",
            "description": "Еженедельное планирование"
        }
    },
    {
        "has_event": False,
        "event": None
    },
    {
        "has_event": True,
        "event": {
            "title": "Презентация",
            "date": "2024-01-17",
            "time": "14:00-15:30",
            "description": "Демонстрация результатов"
        }
    },
    {
        "has_event": False,
        "event": None
    }
]

TEST_CALENDAR_RESULTS = [
    {
        "link": "https://calendar.google.com/event/test1",
        "event_id": "event_id_123"
    },
    {
        "link": "https://calendar.google.com/event/test2",
        "event_id": "event_id_456"
    },
    {
        "link": "https://calendar.google.com/event/test3",
        "event_id": "event_id_789"
    },
    {
        "link": "https://calendar.google.com/event/test4",
        "event_id": "event_id_012"
    },
    {
        "link": "https://calendar.google.com/event/test5",
        "event_id": "event_id_345"
    }
]

TEST_ERRORS = [
    "AI analysis failed",
    "Google Calendar API error",
    "Telegram API error",
    "Network connection failed",
    "Invalid date format",
    "Invalid time format",
    "Configuration file not found",
    "Authentication failed",
    "Rate limit exceeded",
    "Service unavailable"
]

TEST_HTTP_RESPONSES = [
    {
        "status_code": 200,
        "content": '{"ok": true, "result": {"message_id": 123}}'
    },
    {
        "status_code": 400,
        "content": '{"ok": false, "error_code": 400, "description": "Bad Request"}'
    },
    {
        "status_code": 401,
        "content": '{"ok": false, "error_code": 401, "description": "Unauthorized"}'
    },
    {
        "status_code": 429,
        "content": '{"ok": false, "error_code": 429, "description": "Too Many Requests"}'
    },
    {
        "status_code": 500,
        "content": '{"ok": false, "error_code": 500, "description": "Internal Server Error"}'
    }
]

TEST_CALLBACK_DATA = [
    "cancel_event:event_id_123",
    "cancel_event:event_id_456",
    "cancel_event:event_id_789",
    "invalid_callback_data",
    "cancel_event:",
    "cancel_event:event_id_with_spaces",
    "cancel_event:event_id_with_special_chars!@#",
    "cancel_event:very_long_event_id_that_exceeds_normal_length_limits"
]

TEST_TIMESTAMPS = [
    "2024-01-15T15:00:00",
    "2024-01-16T09:00:00",
    "2024-01-17T14:00:00",
    "2024-01-18T00:00:00",
    "2024-01-19T11:00:00"
]

TEST_TIMEZONES = [
    "Europe/Moscow",
    "UTC",
    "America/New_York",
    "Asia/Tokyo",
    "Europe/London"
]

TEST_DATE_FORMATS = [
    "2024-01-15",
    "15.01.2024",
    "15/01/2024",
    "2024-01-15T15:00:00",
    "15 января 2024",
    "January 15, 2024"
]

TEST_TIME_FORMATS = [
    "15:00",
    "15:00-16:00",
    "3:00 PM",
    "15:00:00",
    "15:00-16:30",
    "9:00 AM"
]

def get_random_message():
    import random
    return random.choice(TEST_MESSAGES)

def get_random_event():
    import random
    return random.choice(TEST_EVENTS)

def get_random_metadata():
    import random
    return random.choice(TEST_METADATA)

def get_random_ai_response():
    import random
    return random.choice(TEST_AI_RESPONSES)

def get_random_calendar_result():
    import random
    return random.choice(TEST_CALENDAR_RESULTS)

def get_random_error():
    import random
    return random.choice(TEST_ERRORS)

def get_test_config_with_overrides(**overrides):
    config = TEST_CONFIG.copy()
    config["info"].update(overrides)
    return config

def create_test_event(**overrides):
    base_event = {
        "title": "Тестовое событие",
        "date": "2024-01-15",
        "time": "15:00",
        "description": "Описание события"
    }
    base_event.update(overrides)
    return base_event

def create_test_metadata(**overrides):
    base_metadata = {
        "log_line": "[Тестовый чат] Пользователь: Тестовое сообщение",
        "chat_name": "Тестовый чат",
        "topic_id": None,
        "sender": "Пользователь"
    }
    base_metadata.update(overrides)
    return base_metadata
