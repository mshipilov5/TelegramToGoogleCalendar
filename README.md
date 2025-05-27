# TelegramToGoogleCalendar

📅 TelegramToGoogleCalendar

Проект позволяет автоматически анализировать сообщения из Telegram и добавлять события в Google Calendar с помощью MistralAI через OpenRouter.

🚀 Возможности


	•	Получение сообщений из Telegram


	•	Анализ текста с использованием MistralAI (через OpenRouter API)


	•	Добавление событий в ваш Google Календарь

⸻

⚙️ Подготовка и настройка

1. 🔑 Получение Telegram API ID и Hash
	1.	Перейдите на сайт my.telegram.org.
	2.	Войдите с помощью своего номера телефона.
	3.	Зайдите в раздел API Development Tools.
	4.	Создайте приложение и получите:


	•	api_id


	•	api_hash

⸻

2. 🧠 Получение ключа MistralAI через OpenRouter
	1.	Перейдите на сайт https://openrouter.ai.
	2.	Зарегистрируйтесь и авторизуйтесь.
	3.	Перейдите в раздел API Keys.
	4.	Скопируйте ваш API-ключ.
	5.	Убедитесь, что вы используете модель mistralai/mistral-7b-instruct.

⸻

3. 📅 Настройка доступа к Google Calendar API
	1.	Перейдите в Google Cloud Console.
	2.	Создайте новый проект.
	3.	Включите Google Calendar API.
	4.	Перейдите в Credentials и создайте OAuth 2.0 Client ID:


	•	Тип: Desktop Application


	•	Скачайте credentials.json


	5.	Поместите credentials.json в корень проекта.

⸻

4. 🛠 Настройка конфигурации
	1.	В корне проекта находится файл configTemplate.json.
	2.	Переименуйте его в:
      config.json
 3.	Заполните его своими значениями:
  {
    "telegram_api_id": "ВАШ_API_ID",
    "telegram_api_hash": "ВАШ_API_HASH",
    "openrouter_api_key": "ВАШ_OPENROUTER_API_KEY"
  }

▶️ Запуск
	1.	Установите зависимости:
      pip install -r requirements.txt
  2.	Запустите основной файл:
      python main.py

📝 Примечания
	•	При первом запуске откроется окно авторизации Google — войдите в свою учетную запись.
	•	Проект может работать только при стабильном подключении к интернету.






