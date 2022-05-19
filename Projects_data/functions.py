"""Используемые функции"""

from .variables import ENCODING, MESSAGE_MAX_LENGTH
import json


# Функция получения и декодирования сообщения
def get_message(client):
    code_response = client.recv(MESSAGE_MAX_LENGTH)  # Получение данных в диапазоне от 0 до MESSAGE_MAX_LENGTH(1024)
    if isinstance(code_response, bytes):  # Проверка пременной с данными на формат данных, если не байты, выдаст ошибку
        json_response = code_response.decode(ENCODING)  # Декодировка данных
        response = json.loads(json_response)  # Сохраняем данные в словарь
        if isinstance(response, dict):  # Проверяет,что данные в формате словаря
            return response  # Если все верно вернется словарь
        raise ValueError  # Если не словарь вернет ошибку
    raise ValueError  # Если не байты вернет ошибку


# Функция кодирования и отправки сообщения

def send_message(sock, message):
    _message = json.dumps(message)  # Сериализует словарь в str
    code_message = _message.encode(ENCODING)  # Кодировка _message в ENCODING(utf-8)
    sock.send(code_message)  # Отправка сообщение

