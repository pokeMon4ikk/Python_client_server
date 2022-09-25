"""Unit-тесты клиентской части"""

import unittest
import time

from client import presence_of_client, serv_response
from common.variables import RESPONSE, ERROR


class TestClient(unittest.TestCase):

    def test_presense(self):
        test_1 = presence_of_client()
        self.assertEqual(test_1, {f'action': 'presence', 'time': time.asctime(), 'user': {'account_name': 'Guest'}})

    def test_server_answer_200(self):
        self.assertEqual(serv_response({RESPONSE: 200}), '200 : OK')

    def test_server_answer_400(self):
        self.assertEqual(serv_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_server_no_answer(self):
        self.assertRaises(ValueError, serv_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
