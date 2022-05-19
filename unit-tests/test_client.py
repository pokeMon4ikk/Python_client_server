"""Unit-тесты клиентской части"""

import unittest
import time

from client import presence_of_client, serv_response
from Projects_data.variables import RESPONSE, ERROR


class TestClient(unittest.TestCase):
    """Класс тестов"""

    def test_presense(self):
        """Тест на правильность запроса"""
        test_1 = presence_of_client()
        self.assertEqual(test_1, {f'action': 'presence', 'time': time.asctime(), 'user': {'account_name': 'Guest'}})

    def test_server_answer_200(self):
        """Тест на проверку ответа сервера с кодом 200"""
        self.assertEqual(serv_response({RESPONSE: 200}), '200 : OK')

    def test_server_answer_400(self):
        """Тест на проверку ответа сервера с кодом 400"""
        self.assertEqual(serv_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_server_no_answer(self):
        """Тест на проверку отсутствия ответа сервера"""
        self.assertRaises(ValueError, serv_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
