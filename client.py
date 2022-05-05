import sys
import json
import socket
import time

from Projects_data.functions import get_message, send_message
from Projects_data.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP, \
    DEFAULT_PORT


#  Функция генерации присутствия клиента
def presence_of_client(account_name='Guest'):
    generation_presence = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return generation_presence


# Функция разбора ответа от сервера
def serv_response(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main_func():
    try:
        serv_address = sys.argv[1]
        serv_port = int(sys.argv[2])
        if serv_port < 1024:
            raise ValueError
        elif serv_port > 65535:
            raise ValueError
    except IndexError:
        serv_address = DEFAULT_IP
        serv_port = DEFAULT_PORT
    except ValueError:
        print('Возможно использование портов только в диапазоне от 1024 до 65535!!!')
        sys.exit(1)

    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.connect((serv_address, serv_port))
    message_to_server = presence_of_client()
    send_message(sock_, message_to_server)
    try:
        answer = serv_response(get_message(sock_))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Сообщение от сервера не возможно декодировать!')


if __name__ == '__main__':
    main_func()
