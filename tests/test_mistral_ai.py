import unittest
import json
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai.MistralAI import analyze_message, load_prompt_template, weekday_ru


class TestMistralAI(unittest.TestCase):
    
    def setUp(self):
        self.test_prompt = "Тестовый промпт с {context} и {date_str} для {text}"
        self.test_text = "Встреча завтра в 15:00"
        self.test_context = "рабочие встречи"
        self.mock_client = MagicMock()

        self.mock_response = MagicMock()
        self.mock_response.choices = [MagicMock()]
        self.mock_response.choices[0].message.content = '{"has_event": true, "event": {"title": "Встреча", "date": "2024-01-15", "time": "15:00"}}'
        
        self.mock_client.chat.completions.create.return_value = self.mock_response
    
    def test_weekday_ru_mapping(self):
        expected_days = {
            0: 'понедельник',
            1: 'вторник', 
            2: 'среда',
            3: 'четверг',
            4: 'пятница',
            5: 'суббота',
            6: 'воскресенье'
        }
        
        for day_num, day_name in expected_days.items():
            self.assertEqual(weekday_ru[day_num], day_name)
    
    def test_load_prompt_template_success(self):
        with patch("builtins.open", mock_open(read_data=self.test_prompt)):
            prompt = load_prompt_template()
            
        self.assertEqual(prompt, self.test_prompt)

    def test_load_prompt_template_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError("prompt.txt not found")):
            with self.assertRaises(FileNotFoundError):
                load_prompt_template()

    def test_analyze_message_success(self):
        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", self.test_prompt):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        self.mock_client.chat.completions.create.assert_called_once()
        call_args = self.mock_client.chat.completions.create.call_args

        self.assertEqual(call_args[1]["model"], "mistralai/devstral-small:free")
        self.assertEqual(len(call_args[1]["messages"]), 1)
        self.assertEqual(call_args[1]["messages"][0]["role"], "user")

        self.assertTrue(result["has_event"])
        self.assertIsNotNone(result["event"])
        self.assertEqual(result["event"]["title"], "Встреча")
        self.assertEqual(result["event"]["date"], "2024-01-15")
        self.assertEqual(result["event"]["time"], "15:00")

    def test_analyze_message_with_date_formatting(self):
        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", "Дата: {date_str}"):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        call_args = self.mock_client.chat.completions.create.call_args
        prompt_content = call_args[1]["messages"][0]["content"]

        self.assertIn("сегодня", prompt_content)
        self.assertIn("года", prompt_content)
        self.assertIn(":", prompt_content)  # время

    def test_analyze_message_invalid_json_response(self):
        invalid_response = MagicMock()
        invalid_response.choices = [MagicMock()]
        invalid_response.choices[0].message.content = "invalid json response"

        self.mock_client.chat.completions.create.return_value = invalid_response

        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", self.test_prompt):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        self.assertFalse(result["has_event"])
        self.assertIsNone(result["event"])

    def test_analyze_message_empty_response(self):
        empty_response = MagicMock()
        empty_response.choices = [MagicMock()]
        empty_response.choices[0].message.content = ""

        self.mock_client.chat.completions.create.return_value = empty_response

        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", self.test_prompt):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        self.assertFalse(result["has_event"])
        self.assertIsNone(result["event"])

    def test_analyze_message_no_event_detected(self):
        no_event_response = MagicMock()
        no_event_response.choices = [MagicMock()]
        no_event_response.choices[0].message.content = '{"has_event": false, "event": null}'

        self.mock_client.chat.completions.create.return_value = no_event_response

        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", self.test_prompt):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        self.assertFalse(result["has_event"])
        self.assertIsNone(result["event"])

    def test_analyze_message_client_error(self):
        self.mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", self.test_prompt):
            with self.assertRaises(Exception):
                analyze_message(self.test_text, self.mock_client, self.test_context)

    def test_analyze_message_prompt_formatting(self):
        template = "Контекст: {context}, Дата: {date_str}, Текст: {text}"

        with patch("src.ai.MistralAI.PROMPT_TEMPLATE", template):
            result = analyze_message(self.test_text, self.mock_client, self.test_context)

        call_args = self.mock_client.chat.completions.create.call_args
        prompt_content = call_args[1]["messages"][0]["content"]

        self.assertIn(self.test_context, prompt_content)
        self.assertIn(self.test_text, prompt_content)
        self.assertNotIn("{context}", prompt_content)
        self.assertNotIn("{text}", prompt_content)
        self.assertNotIn("{date_str}", prompt_content)


if __name__ == '__main__':
    unittest.main()
