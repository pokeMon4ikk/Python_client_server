import unittest
import json
import time
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, PRESENCE, \
    TIME, USER, ERROR, ENCODING
from common.utils import get_message, send_message


class SocketForTest:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.code_mes = None
        self.recv_mes = None

    def send(self, send_mes):

        json_test_mes = json.dumps(self.test_dict)
        self.code_mes = json_test_mes.encode(ENCODING)
        self.recv_mes = send_mes

    def recv(self, max_len):

        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):

    test_dict_send = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
        USER: {
            ACCOUNT_NAME: 'test_user'
        }
    }
    test_dict_recv_correct = {RESPONSE: 200}
    test_dict_recv_incorrect = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message(self):

        test_socket = SocketForTest(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.code_mes, test_socket.recv_mes)

    def test_get_message(self):

        test_sock_correct = SocketForTest(self.test_dict_recv_correct)
        test_sock_incorrect = SocketForTest(self.test_dict_recv_incorrect)
        self.assertEqual(get_message(test_sock_correct), self.test_dict_recv_correct)
        self.assertEqual(get_message(test_sock_incorrect), self.test_dict_recv_incorrect)


if __name__ == '__main__':
    unittest.main()
