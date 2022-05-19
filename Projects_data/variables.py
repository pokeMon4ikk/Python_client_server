"""Переменные-константы"""

# Номер порта по умолчанию
DEFAULT_PORT = 9999

# Номер ip по умолчанию
DEFAULT_IP = '127.0.0.1'

# Максимальное количество мест в очереди на подключение
MAX_QUEUE_CONNECTIONS = 3

# Максимальное количество байт для одного сообщения
MESSAGE_MAX_LENGTH = 1024

# Кодировка проекта
ENCODING = 'utf-8'

# Основные ключи в протоколе JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE = 'response'

# Остальные ключи для протокола JIM
PRESENCE = 'presence'
ERROR = 'error'
