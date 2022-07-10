import socket
import sys
import json
import logging
import argparse
import time
import select
import pr_logs.configs.server_log_config

from decorators import log
from Projects_data.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_QUEUE_CONNECTIONS, PRESENCE, \
    TIME, USER, ERROR, DEFAULT_PORT, SENDER, MESSAGE, MESSAGE_TEXT, DEFAULT_IP, EXIT, DESTINATION
from Projects_data.functions import get_message, send_message

# Вызов логгера серверной части
LOGGER = logging.getLogger('server')


@log
def check_client_message(message, messages_list, client, clients, names):
    """Функция проверяющая сообщения клиента"""
    LOGGER.info(f'Информация о сообщении: {message}, полученном от клиента')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, {RESPONSE: 200})
        else:
            response = {RESPONSE: 400, ERROR: 'Имя пользователя уже занято.'}
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message and \
            SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        response = {RESPONSE: 400, ERROR: 'Запрос некорректен.'}
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='', nargs='?')
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    if 1023 > listen_port or listen_port > 65536:
        LOGGER.critical(f'Некорректный номер порта. Допустимые порты от 1023 до 65536')
        sys.exit(1)
    return listen_address, listen_port


def main_func():
    listen_address, listen_port = arg_parser()

    LOGGER.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.bind((listen_address, listen_port))
    sock_.settimeout(0.5)

    clients = []
    messages = []

    names = dict()

    while True:
        try:
            client, client_address = sock_.accept()
        except Exception:
            pass

        else:
            LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    check_client_message(get_message(client_with_message), messages, client_with_message, clients, names)
                except Exception:
                    LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main_func()
