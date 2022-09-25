"""Конфиг-файл для логгов серверной-части приложения"""

import logging
from logging import handlers
import os
import sys
from common.variables import LOGGING_LEVEL

PATH = 'pr_logs/logs/server_logs'
PATH = os.path.join(PATH, 'server.log')

CLIENT_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf8', interval=1, when='midnight')
LOG_FILE.setFormatter(CLIENT_FORMATTER)
LOG_STREAM = logging.StreamHandler(sys.stderr)
LOG_STREAM.setFormatter(CLIENT_FORMATTER)
LOG_STREAM.setLevel(logging.CRITICAL)

LOGGER = logging.getLogger('server')
LOGGER.addHandler(LOG_FILE)
LOGGER.addHandler(LOG_STREAM)
LOGGER.setLevel(LOGGING_LEVEL)

if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.warning('Предупреждение')
    LOGGER.info('Информационное сообщение')
    LOGGER.debug('Отладочная информация')