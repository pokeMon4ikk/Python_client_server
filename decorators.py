"""Декораторы"""

import pr_logs.configs.server_log_config
import pr_logs.configs.client_log_config
import sys
import logging
import inspect


if sys.argv[0].find('client') == -1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')


def log(log_function):
    """Декоратор логгов в виде функции"""

    def log_wrap(*args, **kwargs):
        res = log_function(*args, **kwargs)
        LOGGER.info(f" Вызов функции {log_function.__name__} с параметрами {args}, {kwargs} "
                    f"из модуля {log_function.__module__}. Вызов из функции {inspect.stack()[1][3]}", stacklevel=2)
        return res
    return log_wrap


class Log:
    """Декоратор логгов в виде класса"""
    def __call__(self, log_func):
        def log_wrap(*args, **kwargs):
            res = log_func(*args, **kwargs)
            LOGGER.info(f" Вызов функции {log_func.__name__} с параметрами {args}, {kwargs} "
                        f"из модуля {log_func.__module__}. Вызов из функции {inspect.stack()[1][3]}", stacklevel=2)
            return res
        return log_wrap

