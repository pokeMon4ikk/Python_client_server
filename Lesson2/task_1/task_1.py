"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import re
import csv


def get_data():
    producers = []
    names_Os = []
    code = []
    type_of_system = []
    fin_content_for_csv = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']

    for file in files_list:
        opening_files = open(file).read()  # Открываем все файлы и читаем содержимое всех этих файлов

        reg_prod = re.compile(r'\w{12}\s*\w{7}\D\s*\w{4,6}')  # Изготовители системы
        reg_prod_data = reg_prod.findall(opening_files)
        for prods in reg_prod_data:
            prod = prods[34:]
            producers.append(prod)

        reg_name = re.compile(r'\w{8}\s*\w{2}\D\s*\w{9}\s*\w{7}\s\S*')  # Название ОС
        reg_name_data = reg_name.findall(opening_files)
        for names in reg_name_data:
            name = names[44:]
            names_Os.append(name)

        reg_code = re.compile(r'\w{3}\s*\w{8}\D\s*\d{5}\D\w{3}\D\d{7}\D\d{5}')  # Код продукта
        reg_code_data = reg_code.findall(opening_files)
        for codes in reg_code_data:
            code_ = codes[34:]
            code.append(code_)

        reg_type = re.compile(r'\w{3}\s*\w{7}\D\s*\w\d{2}\D\w{5}\s*\w{2}')  # Тип системы
        reg_type_data = reg_type.findall(opening_files)
        for types in reg_type_data:
            type_ = types[34:]
            type_of_system.append(type_)

    fin_content_for_csv.append(headers)  # добавляем хедеры в основной списсок данных

    for i in range(0, 3):  # вносим остальные данные в основной список данных
        fin_cont = []
        fin_cont.append(producers[i])
        fin_cont.append(names_Os[i])
        fin_cont.append(code[i])
        fin_cont.append(type_of_system[i])
        fin_content_for_csv.append(fin_cont)
    return fin_content_for_csv


def write_to_csv(file_name):  # дбавляем основной массив данных в csv-файл
    data = get_data()
    with open(file_name, 'w', encoding='utf-8') as file:
        writing = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in data:
            writing.writerow(row)


write_to_csv('report.csv')  # выполням создание csv-файла

