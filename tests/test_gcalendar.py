import unittest
import tempfile
import os
import json
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calendar.GCalendar import create_event_in_calendar, delete_event_from_calendar, delete_handler_async


class TestGCalendar(unittest.TestCase):
    
    def setUp(self):
        self.test_event_with_time = {
            "title": "Тестовая встреча",
            "date": "2024-01-15",
            "time": "15:00-16:00",
            "description": "Описание встречи"
        }
        
        self.test_event_without_time = {
            "title": "Тестовое событие",
            "date": "2024-01-15",
            "description": "Описание события"
        }
        
        self.test_event_single_time = {
            "title": "Короткая встреча",
            "date": "2024-01-15",
            "time": "14:00",
            "description": "Встреча на час"
        }

        self.mock_service = MagicMock()
        self.mock_event_result = MagicMock()
        self.mock_event_result.get.return_value = "test_event_id"
        self.mock_event_result.get.side_effect = lambda key: {
            "id": "test_event_id",
            "htmlLink": "https://calendar.google.com/event/test"
        }.get(key)
        
        self.mock_service.events.return_value.insert.return_value.execute.return_value = self.mock_event_result

    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.InstalledAppFlow')
    @patch('src.calendar.GCalendar.Credentials')
    @patch('os.path.exists')
    def test_create_event_in_calendar_invalid_time_format(self, mock_exists, mock_creds, mock_flow, mock_build):
        mock_exists.return_value = True
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service
        
        invalid_event = {
            "title": "Тест",
            "date": "2024-01-15",
            "time": "invalid_time_format",
            "description": "Описание"
        }
        
        result = create_event_in_calendar(invalid_event)

        self.assertIsNone(result)
    
    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.InstalledAppFlow')
    @patch('src.calendar.GCalendar.Credentials')
    @patch('os.path.exists')
    def test_create_event_in_calendar_invalid_date_format(self, mock_exists, mock_creds, mock_flow, mock_build):
        mock_exists.return_value = True
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service
        
        invalid_event = {
            "title": "Тест",
            "date": "invalid_date",
            "description": "Описание"
        }
        
        result = create_event_in_calendar(invalid_event)

        self.assertIsNone(result)
    
    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.InstalledAppFlow')
    @patch('src.calendar.GCalendar.Credentials')
    @patch('os.path.exists')
    def test_create_event_in_calendar_api_error(self, mock_exists, mock_creds, mock_flow, mock_build):
        mock_exists.return_value = True
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service

        self.mock_service.events.return_value.insert.return_value.execute.side_effect = Exception("API Error")
        
        result = create_event_in_calendar(self.test_event_with_time)

        self.assertIsNone(result)
    
    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.Credentials')
    def test_delete_event_from_calendar_success(self, mock_creds, mock_build):
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service
        
        result = delete_event_from_calendar("test_event_id")
        
        self.assertTrue(result)
        self.mock_service.events.return_value.delete.assert_called_once_with(
            calendarId='primary', 
            eventId='test_event_id'
        )
    
    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.Credentials')
    def test_delete_event_from_calendar_already_deleted(self, mock_creds, mock_build):
        from googleapiclient.errors import HttpError
        
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service

        mock_response = MagicMock()
        mock_response.status = 410
        http_error = HttpError(mock_response, b"Already deleted")
        
        self.mock_service.events.return_value.delete.return_value.execute.side_effect = http_error
        
        result = delete_event_from_calendar("test_event_id")
        
        self.assertFalse(result)
    
    @patch('src.calendar.GCalendar.build')
    @patch('src.calendar.GCalendar.Credentials')
    def test_delete_event_from_calendar_other_error(self, mock_creds, mock_build):
        from googleapiclient.errors import HttpError
        
        mock_creds.from_authorized_user_file.return_value = MagicMock()
        mock_build.return_value = self.mock_service

        mock_response = MagicMock()
        mock_response.status = 500
        http_error = HttpError(mock_response, b"Server error")
        
        self.mock_service.events.return_value.delete.return_value.execute.side_effect = http_error
        
        with self.assertRaises(HttpError):
            delete_event_from_calendar("test_event_id")
    
    @patch('src.calendar.GCalendar.delete_event_from_calendar')
    def test_delete_handler_async(self, mock_delete):
        import asyncio
        
        mock_delete.return_value = True
        
        async def test_async():
            result = await delete_handler_async("test_event_id")
            return result
        
        result = asyncio.run(test_async())
        
        self.assertTrue(result)
        mock_delete.assert_called_once_with("test_event_id")


if __name__ == '__main__':
    unittest.main()
