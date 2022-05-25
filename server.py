import socket
import sys
import json
import logging
import pr_logs.configs.server_log_config

from  decorators import log
from Projects_data.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_QUEUE_CONNECTIONS, PRESENCE, \
    TIME, USER, ERROR, DEFAULT_PORT
from Projects_data.functions import get_message, send_message

# Вызов логгера серверной части
LOGGER = logging.getLogger('server')


# Функция проверяющая сообщения клиента
@log
def check_client_message(message):
    LOGGER.info(f'Информация о сообщении: {message}, полученном от клиента')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main_func():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            LOGGER.info(f'Номер порта подключения: {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            LOGGER.info(f'Портом подключения выбран дефолтный порт: {listen_port}')
        if listen_port < 1024 or listen_port > 65535:
            LOGGER.error(f'Номер порта подключения: {listen_port} указан неверно!')
            raise ValueError
    except IndexError:
        LOGGER.error('После параметра -\'p\' следует указать номер порта в диапазоне от 1024 до 65535!!! .')
        sys.exit(1)
    except ValueError:
        LOGGER.error('Номером порта должно быть число в диапазоне от 1024 до 65535!!!')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
            LOGGER.info(f'Адрес подключения: {listen_address}')
        else:
            listen_address = ''
            LOGGER.warning(f'Адрес подключения не указан!')
    except IndexError:
        LOGGER.error('После параметра \'a\'- следует указать адрес!')
        sys.exit(1)

    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.bind((listen_address, listen_port))
    sock_.listen(MAX_QUEUE_CONNECTIONS)

    while True:
        client, client_address = sock_.accept()
        try:
            message_from = get_message(client)
            LOGGER.info(f'Получено сообщение: {message_from}')
            response = check_client_message(message_from)
            LOGGER.info(f'Сформирован ответ: {response}')
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            LOGGER.error('Клиент отправил некорректное сообщение.')
            client.close()


if __name__ == '__main__':
    main_func()
