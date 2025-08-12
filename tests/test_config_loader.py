import unittest
import json
import tempfile
import os
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.configLoader import load_config


class TestConfigLoader(unittest.TestCase):
    
    def setUp(self):
        self.test_config = {
            "info": {
                "mistralAI_key": "test_key_123",
                "telegram_API_ID": "12345",
                "telegram_API_hash": "test_hash_abc",
                "name": "TestBot",
                "TARGET_CHATS": ["chat1", "chat2"],
                "telegram_notify_token": "bot_token_123",
                "telegram_notify_chat_id": "chat_id_123",
                "context": "test_context"
            }
        }
    
    def test_load_config_success(self):
        with patch("builtins.open", mock_open(read_data=json.dumps(self.test_config))):
            config = load_config()
            
        expected_config = self.test_config["info"]
        self.assertEqual(config, expected_config)
        self.assertEqual(config["mistralAI_key"], "test_key_123")
        self.assertEqual(config["telegram_API_ID"], "12345")
        self.assertEqual(config["name"], "TestBot")
    
    def test_load_config_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError("config.json not found")):
            with self.assertRaises(FileNotFoundError):
                load_config()
    
    def test_load_config_invalid_json(self):
        invalid_json = "{ invalid json content }"
        with patch("builtins.open", mock_open(read_data=invalid_json)):
            with self.assertRaises(json.JSONDecodeError):
                load_config()
    
    def test_load_config_missing_info_key(self):
        config_without_info = {"other_key": "value"}
        with patch("builtins.open", mock_open(read_data=json.dumps(config_without_info))):
            with self.assertRaises(KeyError):
                load_config()
    
    def test_load_config_encoding(self):
        config_with_cyrillic = {
            "info": {
                "name": "ТестовыйБот",
                "context": "Тестовый контекст"
            }
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(config_with_cyrillic, ensure_ascii=False))):
            config = load_config()
            
        self.assertEqual(config["name"], "ТестовыйБот")
        self.assertEqual(config["context"], "Тестовый контекст")
    
    def test_load_config_empty_info(self):
        empty_config = {"info": {}}
        with patch("builtins.open", mock_open(read_data=json.dumps(empty_config))):
            config = load_config()
            
        self.assertEqual(config, {})


if __name__ == '__main__':
    unittest.main()
