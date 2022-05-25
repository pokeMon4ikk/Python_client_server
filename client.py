import sys
import json
import socket
import time
import logging
from decorators import log

from Projects_data.functions import get_message, send_message
from Projects_data.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP, \
    DEFAULT_PORT
import pr_logs.configs.client_log_config

# Вызов логгера клиентской части
LOGGER = logging.getLogger('client')


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
    LOGGER.info(f'От сервера получен ответ: {RESPONSE}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    LOGGER.critical(f'Ответ от сервера не получен!!!')
    raise ValueError


def main_func():
    try:
        serv_address = sys.argv[1]
        serv_port = int(sys.argv[2])
        LOGGER.info(f'Клиент с адресом:{serv_address} и портом: {serv_port} запущен')
        if serv_port < 1024:
            LOGGER.error(f'Номер порта {serv_port} указан неверно!')
            raise ValueError
        elif serv_port > 65535:
            LOGGER.error(f'Номер порта {serv_port} указан неверно!')
            raise ValueError
    except IndexError:
        serv_address = DEFAULT_IP
        serv_port = DEFAULT_PORT
    except ValueError:
        LOGGER.error(f'Возможно использование портов только в диапазоне от 1024 до 65535!!!')
        sys.exit(1)

    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.connect((serv_address, serv_port))
    message_to_server = presence_of_client()
    send_message(sock_, message_to_server)
    try:
        answer = serv_response(get_message(sock_))
        LOGGER.info(f'Принят ответ от сервера {answer}')
    except (ValueError, json.JSONDecodeError):
        LOGGER.error(f'Сообщение от сервера не возможно декодировать!')


if __name__ == '__main__':
    main_func()
