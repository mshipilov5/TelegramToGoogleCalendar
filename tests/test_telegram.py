import unittest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.telegram.TelegramListener import start_telegram_listener

class TestTelegramListener(unittest.TestCase):

    def setUp(self):
        self.test_config = {
            "telegram_API_ID": "12345",
            "telegram_API_hash": "test_hash_abc",
            "TARGET_CHATS": ["chat1", "chat2", "chat3"]
        }

        self.test_callback = AsyncMock()

        self.mock_client = MagicMock()
        self.mock_client.start = AsyncMock()
        self.mock_client.run_until_disconnected = AsyncMock()

    @patch('src.telegram.TelegramListener.TelegramClient')
    def test_start_telegram_listener_success(self, mock_telegram_client):
        mock_telegram_client.return_value = self.mock_client

        async def test_async():
            await start_telegram_listener(self.test_callback, self.test_config)

        asyncio.run(test_async())

        mock_telegram_client.assert_called_once_with('session_name', 12345, 'test_hash_abc')

        self.mock_client.start.assert_called_once()
        self.mock_client.run_until_disconnected.assert_called_once()

    @patch('src.telegram.TelegramListener.TelegramClient')
    def test_start_telegram_listener_config_parsing(self, mock_telegram_client):
        mock_telegram_client.return_value = self.mock_client

        config_with_int_id = {
            "telegram_API_ID": 12345,
            "telegram_API_hash": "test_hash",
            "TARGET_CHATS": ["chat1"]
        }

        async def test_async():
            await start_telegram_listener(self.test_callback, config_with_int_id)

        asyncio.run(test_async())

        mock_telegram_client.assert_called_once_with('session_name', 12345, 'test_hash')

    @patch('src.telegram.TelegramListener.TelegramClient')
    def test_start_telegram_listener_empty_target_chats(self, mock_telegram_client):
        mock_telegram_client.return_value = self.mock_client

        config_empty_chats = {
            "telegram_API_ID": "12345",
            "telegram_API_hash": "test_hash",
            "TARGET_CHATS": []
        }

        async def test_async():
            await start_telegram_listener(self.test_callback, config_empty_chats)

        asyncio.run(test_async())

        mock_telegram_client.assert_called_once()

    @patch('src.telegram.TelegramListener.TelegramClient')
    def test_start_telegram_listener_client_start_error(self, mock_telegram_client):
        mock_telegram_client.return_value = self.mock_client
        self.mock_client.start.side_effect = Exception("Connection failed")

        async def test_async():
            with self.assertRaises(Exception):
                await start_telegram_listener(self.test_callback, self.test_config)

        asyncio.run(test_async())

    @patch('src.telegram.TelegramListener.TelegramClient')
    def test_start_telegram_listener_event_handler_registration(self, mock_telegram_client):
        mock_telegram_client.return_value = self.mock_client

        async def test_async():
            await start_telegram_listener(self.test_callback, self.test_config)

        asyncio.run(test_async())

        self.mock_client.on.assert_called_once()


if __name__ == '__main__':
    unittest.main()