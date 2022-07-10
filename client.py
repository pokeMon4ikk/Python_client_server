import sys
import json
import socket
import time
import logging
from decorators import log
import argparse
import threading

from Projects_data.functions import get_message, send_message
from Projects_data.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP, \
    DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT, EXIT, DESTINATION
import pr_logs.configs.client_log_config

# Вызов логгера клиентской части
LOGGER = logging.getLogger('client')


@log
def message_for_exit(account_name):
    """Функция генерирует сообщение о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.asctime(),
        ACCOUNT_NAME: account_name
    }


@log
def server_message(sock, user):
    """Функция обрабатывает сообщения с сервера от других пользователей"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == user:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                            f'\n{message[MESSAGE_TEXT]}')
            else:
                LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOGGER.critical(f'Потеряно соединение с сервером.')
            break


def message_creation(sock, account_name='Guest'):
    """Функция создания сообщения клиентом, при нажатии 'Q' она завершает свою работу """
    to_user = input('Введите имя получателя вашего сообщения : ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.asctime(),
        MESSAGE_TEXT: message
    }
    LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        LOGGER.info(f'Отправлено сообщение для пользователя {to_user}')
    except:
        LOGGER.critical('Соединение с сервером прервано!')
        sys.exit(1)

@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            message_creation(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, message_for_exit(username))
            print('Завершение соединения.')
            LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def presence_of_client(account_name):
    """Функция генерации присутствия клиента"""
    generation_presence = {
        ACTION: PRESENCE,
        TIME: time.asctime(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    LOGGER.info(f'Для пользователя с никнеймом аккаунта {account_name} сгенерировано {PRESENCE}')
    return generation_presence


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')

@log
def serv_response(message):
    """Функция разбора ответа от сервера"""
    LOGGER.info(f'От сервера полученo сообщение: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    LOGGER.critical(f'Ответ от сервера не получен!!!')
    raise Exception


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if 1023 > server_port or server_port > 65536:
        LOGGER.critical(f'Некорректный номер порта. Допустимые порты от 1023 до 65536')
        sys.exit(1)

    return server_address, server_port, client_name


def main_func():
    print('Консольный месседжер. Клиентский модуль.')

    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    LOGGER.info(
        f'Запущен клиент с адресом: {server_address} на порту: {server_port} с режимом работы: {client_name}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, presence_of_client(client_name))
        answer = serv_response(get_message(transport))
        LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:

        receiver = threading.Thread(target=server_message, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main_func()
