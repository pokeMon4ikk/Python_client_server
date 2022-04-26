"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import chardet
import subprocess
import os


command_1 = ['ping', 'yandex.ru']
command_2 = ['ping', 'youtube.com']

ping_yandex = subprocess.Popen(command_1, stdout=subprocess.PIPE)
print(ping_yandex.stdout)
for b_line in ping_yandex.stdout:
    result = chardet.detect(b_line)
    # print(result)
    b_line = b_line.decode(result['encoding']).encode('utf-8')
    print(b_line.decode('utf-8'))

ping_youtube = subprocess.Popen(command_2, stdout=subprocess.PIPE)
print(ping_youtube.stdout)
for bt_line in ping_youtube.stdout:
    result_ = chardet.detect(bt_line)
    # print(result_)
    bt_line = bt_line.decode(result_['encoding']).encode('utf-8')
    print(bt_line.decode('utf-8'))
