"""Unit-тесты серверной части"""

import unittest
import time
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import check_client_message


class TestServer(unittest.TestCase):
    """Класс тестов(на серверной части всего одна функция для тестов)"""

    correct_response = {RESPONSE: 200}

    incorrect_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_correct_data(self):
        """Тест на правильные данные"""
        self.assertEqual(check_client_message({ACTION: 'presence', TIME: time.asctime(),
                                               USER: {ACCOUNT_NAME: 'Guest'}}), self.correct_response)

    def test_no_time(self):
        """Тест на отсутствие времени"""
        self.assertEqual(check_client_message({ACTION: 'presence', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.incorrect_response)

    def test_no_action(self):
        """Тест на отсутствие действия"""
        self.assertEqual(check_client_message({TIME: time.asctime(), USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.incorrect_response)

    def test_no_user(self):
        """Тест на отсутствие пользователя"""
        self.assertEqual(check_client_message({ACTION: 'some different action', TIME: time.asctime()}),
                         self.incorrect_response)

    def test_other_action(self):
        """Тест на другое действие"""
        self.assertEqual(check_client_message({ACTION: 'some different action', TIME: time.asctime(),
                                               USER: {ACCOUNT_NAME: 'Guest'}}), self.incorrect_response)

    def test_other_user(self):
        """Тест на другого пользоватекя"""
        self.assertEqual(check_client_message({ACTION: 'presence', TIME: time.asctime(),
                                               USER: {ACCOUNT_NAME: 'other_user'}}), self.incorrect_response)

    def test_no_action_no_time(self):
        """Тест на отсутствие действия и времени"""
        self.assertEqual(check_client_message({USER: {ACCOUNT_NAME: 'Guest'}}), self.incorrect_response)

    def test_no_action_no_user(self):
        """Тест на отсутствие действия и пользователя"""
        self.assertEqual(check_client_message({TIME: time.asctime()}), self.incorrect_response)

    def test_no_time_no_user(self):
        """Тест на отсутствие времени и пользователя"""
        self.assertEqual(check_client_message({ACTION: 'presence'}), self.incorrect_response)

    def test_no_time_other_user(self):
        """Тест на отсутствие времени и другого пользователя"""
        self.assertEqual(check_client_message({ACTION: 'presence', USER: {ACCOUNT_NAME: 'other_user'}}),
                         self.incorrect_response)

    def test_other_action_other_user(self):
        """Тест на другое действие и другого пользователя"""
        self.assertEqual(check_client_message({ACTION: 'message', TIME: time.asctime(),
                                               USER: {ACCOUNT_NAME: 'other_user'}}), self.incorrect_response)

    def test_no_action_other_user(self):
        """Тест на отсутствие действия и другого пользователя"""
        self.assertEqual(check_client_message({TIME: time.asctime(),
                                               USER: {ACCOUNT_NAME: 'other_user'}}), self.incorrect_response)


if __name__ == '__main__':
    unittest.main()
