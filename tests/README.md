# Тесты для проекта TelegramToGoogleCalendar

Этот каталог содержит модульные тесты для всех компонентов проекта.

## Структура тестов

- `test_config_loader.py` - тесты для модуля загрузки конфигурации
- `test_mistral_ai.py` - тесты для модуля анализа сообщений с помощью ИИ
- `test_gcalendar.py` - тесты для модуля работы с Google Calendar
- `test_telegram.py` - тесты для модуля Telegram
- `test_data.py` - тестовые данные и константы
- `run_tests.py` - скрипт для запуска всех тестов

## Установка зависимостей для тестирования

```bash
pip install -r tests/requirements.txt
```

## Запуск тестов

### Запуск всех тестов

```bash
# Из корневой директории проекта
python tests/run_tests.py

# Или с помощью unittest
python -m unittest discover tests -v
```

### Запуск конкретного модуля тестов

```bash
# Тесты для configLoader
python tests/run_tests.py test_config_loader

# Тесты для MistralAI
python tests/run_tests.py test_mistral_ai

# И так далее для других модулей
```

### Запуск отдельных тестов

```bash
# Тесты для конкретного класса
python -m unittest tests.test_config_loader.TestConfigLoader -v

# Конкретный тест
python -m unittest tests.test_config_loader.TestConfigLoader.test_load_config_success -v
```

## Запуск с помощью pytest (рекомендуется)

```bash
# Установка pytest
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Запуск всех тестов
pytest tests/ -v

# Запуск с покрытием кода
pytest tests/ --cov=. --cov-report=html

# Запуск конкретного модуля
pytest tests/test_config_loader.py -v
```

## Особенности тестирования

### Асинхронные тесты

Многие функции в проекте асинхронные. Для их тестирования используется:
- `unittest.mock.AsyncMock` для моков асинхронных функций
- `asyncio.run()` для запуска асинхронных тестов

### Моки внешних API

Тесты используют моки для:
- OpenAI API (MistralAI)
- Google Calendar API
- Telegram API
- HTTP запросов

### Тестовые данные

Тесты включают различные сценарии:
- Успешные операции
- Обработка ошибок
- Граничные случаи
- Некорректные данные

## Примеры тестов

### Тест загрузки конфигурации

```python
def test_load_config_success(self):
    """Тест успешной загрузки конфигурации"""
    with patch("builtins.open", mock_open(read_data=json.dumps(self.test_config))):
        config = load_config()
        
    expected_config = self.test_config["info"]
    self.assertEqual(config, expected_config)
```

### Тест асинхронной функции

```python
async def test_async_function(self):
    """Тест асинхронной функции"""
    result = await some_async_function()
    self.assertIsNotNone(result)
```

## Добавление новых тестов

1. Создайте новый файл `test_module_name.py`
2. Наследуйтесь от `unittest.TestCase`
3. Добавьте файл в список в `run_tests.py`
4. Следуйте существующим паттернам именования и структуры

## Покрытие кода

Для анализа покрытия кода тестами:

```bash
# Установка coverage
pip install coverage

# Запуск тестов с покрытием
coverage run -m unittest discover tests
coverage report
coverage html  # Создает HTML отчет
```

## Отладка тестов

Для отладки конкретного теста:

```python
import pdb; pdb.set_trace()  # Точка останова
```

Или используйте `pytest --pdb` для автоматической остановки на ошибках.

## CI/CD интеграция

Тесты можно интегрировать в CI/CD pipeline:

```yaml
# Пример для GitHub Actions
- name: Run tests
  run: |
    python tests/run_tests.py
    pytest tests/ --cov=. --cov-report=xml
```

## Полезные команды

```bash
# Быстрый запуск тестов
python tests/run_tests.py

# Тесты с подробным выводом
python -m unittest discover tests -v

# Тесты конкретного модуля
python tests/run_tests.py test_gcalendar

# Запуск с pytest
pytest tests/ -v -s

# Тесты с покрытием
pytest tests/ --cov=. --cov-report=term-missing
```
