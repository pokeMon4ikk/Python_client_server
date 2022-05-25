"""Конфиг-файл для логгов клиент-части приложения"""

import logging
import os
import sys
from Projects_data.variables import LOGGING_LEVEL

# Подготовка названия файла для логгирования, а также пути его сохранения
PATH = 'pr_logs/logs/client_logs'
PATH = os.path.join(PATH, 'client.log')

# Создание форматтера
CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Вывод логгов
LOG_FILE = logging.FileHandler(PATH, encoding='utf8')
LOG_FILE.setFormatter(CLIENT_FORMATTER)
LOG_STREAM = logging.StreamHandler(sys.stderr)
LOG_STREAM.setFormatter(CLIENT_FORMATTER)
LOG_STREAM.setLevel(logging.CRITICAL)

# Создание регистратора
LOGGER = logging.getLogger('client')
LOGGER.addHandler(LOG_FILE)
LOGGER.addHandler(LOG_STREAM)
LOGGER.setLevel(LOGGING_LEVEL)

# Отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.info('Информационное сообщение')
    LOGGER.debug('Отладочная информация')





