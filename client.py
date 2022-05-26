import sys
import json
import socket
import time
import logging
from decorators import log
import argparse

from Projects_data.functions import get_message, send_message
from Projects_data.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP, \
    DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT
import pr_logs.configs.client_log_config

# Вызов логгера клиентской части
LOGGER = logging.getLogger('client')


@log
def server_message(message):
    """Функция обрабатывает сообщения с сервера от других пользователей"""
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение {message[MESSAGE_TEXT]} от пользователя {message[SENDER]}')
        LOGGER.info(f'Получено сообщение {message[MESSAGE_TEXT]} от пользователя {message[SENDER]}')
    else:
        LOGGER.error(f'Сообщение {message} имеет некорректный формат')


def message_creation(sock, account_name='Guest'):
    """Функция создания сообщения клиентом, при нажатии 'Q' она завершает свою работу """

    user_decision = '\\q'
    message = input(f'Введите ваще сообщение или {user_decision} для завершения работы: ')
    if MESSAGE == user_decision:
        sock.close()
        LOGGER.info('Пользователь завершил работу!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.asctime(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформировано сообщение: {message_dict}')
    return message_dict


#  Функция генерации присутствия клиента
@log
def presence_of_client(account_name='Guest'):
    generation_presence = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.info(f'Для пользователя {USER} с никнеймом аккаунта {ACCOUNT_NAME} сгенерировано {PRESENCE}')
    return generation_presence


# Функция разбора ответа от сервера
@log
def serv_response(message):
    LOGGER.info(f'От сервера полученo сообщение: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    LOGGER.critical(f'Ответ от сервера не получен!!!')
    raise ValueError


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    serv_address = namespace.addr
    serv_port = namespace.port
    client_mode = namespace.mode

    if 1023 > serv_port or serv_port > 65536:
        LOGGER.critical(f'Некорректный номер порта. Допустимые порты от 1023 до 65536')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        LOGGER.critical(f'Недопустимый режим работы {client_mode}')
        sys.exit(1)

    return serv_address, serv_port, client_mode


def main_func():
    serv_address, serv_port, client_mode = arg_parser()

    LOGGER.info(
        f'Запущен клиент с адресом: {serv_address} на порту: {serv_port} с режимом работы: {client_mode}')

    try:
        sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_.connect((serv_address, serv_port))
        send_message(sock_, presence_of_client())
        answer = serv_response(get_message(sock_))
        LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        LOGGER.error(f'Сообщение от сервера не возможно декодировать!')
        sys.exit(1)
    except ConnectionRefusedError:
        LOGGER.critical(
            f'Не удалось подключиться к серверу {serv_address}:{serv_port}')
        sys.exit(1)
    else:
        if client_mode == 'listen':
            print('Режим работы - приём сообщений.')
        else:
            print('Режим работы - отправка сообщений.')
        while True:
            if client_mode == 'send':
                try:
                    send_message(sock_, message_creation(sock_))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.warning(f'Соединение с сервером {serv_address} прервано!')
                    sys.exit(1)

            if client_mode == 'listen':
                try:
                    server_message(get_message(sock_))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOGGER.warning(f'Соединение с сервером {serv_address} прервано!')
                    sys.exit(1)


if __name__ == '__main__':
    main_func()
