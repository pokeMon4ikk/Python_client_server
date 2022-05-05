import socket
import sys
import json

from Projects_data.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_QUEUE_CONNECTIONS, PRESENCE, \
    TIME, USER, ERROR, DEFAULT_PORT
from Projects_data.functions import get_message, send_message


# Функция проверяющая сообщения клиента
def check_client_message(message):
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
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' следует указать номер порта в диапазоне от 1024 до 65535!!! .')
        sys.exit(1)
    except ValueError:
        print(
            'Номером порта должно быть число в диапазоне от 1024 до 65535!!!')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        print(
            'После параметра \'a\'- следует указать адрес.')
        sys.exit(1)

    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.bind((listen_address, listen_port))

    sock_.listen(MAX_QUEUE_CONNECTIONS)

    while True:
        client, client_address = sock_.accept()
        try:
            message_from = get_message(client)
            print(message_from)
            response = check_client_message(message_from)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Клиент отправил некорректное сообщение.')
            client.close()


if __name__ == '__main__':
    main_func()
