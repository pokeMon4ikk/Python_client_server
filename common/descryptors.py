import logging
import sys

if sys.argv[0].find("client_dist") == -1:
    logger = logging.getLogger("server_dist")
else:
    logger = logging.getLogger("client_dist")


class Port:

    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f"Попытка запуска с указанием неподходящего порта {value}. Допустимы адреса с 1024 до 65535."
            )
            raise TypeError("Некорректрый номер порта")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
