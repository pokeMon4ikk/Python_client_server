"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""

import yaml


data = {'name': ['Grisha Glinkin', 'Grisha Julikov', 'Grisha Fedotov', 'Grisha Sedoy'],
        'wife_quantity': 1,
        'salary': {'Grisha Glinkin': '10000￥', 'Grisha Julikov': '20000￥',
                   'Grisha Fedotov': '30000￥', 'Grisha Sedoy': '40000￥'}
        }

with open('file.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as file_2:
    data_ = yaml.load(file_2, Loader=yaml.SafeLoader)

print(data == data_)
