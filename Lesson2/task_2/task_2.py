"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать запись
данных в виде словаря в файл orders.json. При записи данных указать
величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.

ПРОШУ ВАС НЕ УДАЛЯТЬ ИСХОДНЫЙ JSON-ФАЙЛ
ПРИМЕР ТОГО, ЧТО ДОЛЖНО ПОЛУЧИТЬСЯ

{
    "orders": [
        {
            "item": "printer",
            "quantity": "10",
            "price": "6700",
            "buyer": "Ivanov I.I.",
            "date": "24.09.2017"
        },
        {
            "item": "scaner",
            "quantity": "20",
            "price": "10000",
            "buyer": "Petrov P.P.",
            "date": "11.01.2018"
        }
    ]
}

вам нужно подгрузить JSON-объект
и достучаться до списка, который и нужно пополнять
а потом сохранять все в файл
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r', encoding='utf-8') as file:
        # читаем файл,чтобы получить его содержимое и сохраняем в переменную
        data = json.load(file)

    # записываем данные в файл
    with open('orders.json', 'w', encoding='utf-8') as file_json:
        orders = data['orders']
        order = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
        orders.append(order)
        json.dump(data, file_json, indent=4)


write_order_to_json('TV', '5', '200000', 'Grisha Julikov', '19.05.2021')
write_order_to_json('Sofa', '1', '35000', 'Grisha Fedotov', '27.05.2021')
write_order_to_json('wardrobe', '3', '144000', 'Grisha Sedoy', '30.12.2021')
write_order_to_json('mirror', '2', '16000', 'Grisha Glinkin', '02.07.2011')
