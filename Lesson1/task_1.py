"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

"""

# Вариант 1 - Самый простой - просмотр в декодере

word_list_1 = ['разработка', 'сокет', 'декоратор']
for word in word_list_1:
    print(word)
    print(type(word))

word_list_2 = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0441\u043e\u043a\u0435\u0442',
               '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
for word in word_list_2:
    print(word)
    print(type(word))

# Вариант 2 средняя сложность - работа со строкой

word_list_4 = ['разработка', 'сокет', 'декоратор']
for word in word_list_4:
    new = ''.join('\\u{:04x}'.format(ord(c)) for c in word)
    unicode_1 = new.encode('utf-8').decode('unicode-escape')
    print(unicode_1)
    print(type(unicode_1))

# Вариант 3 самый запарный - преобразование байтов в строку и работа с ней

word_list_3 = ['разработка', 'сокет', 'декоратор']
for word in word_list_3:
    words = str(word.encode('unicode_escape')).replace("\\\\", ' ')[3:-1]  # получаем нужные ззначения в байтах
    # и приводим их в строку, обрезая лишнее
    words_ = chr(92) + chr(92).join(words.split())
    unicode_2 = words_.encode('utf-8').decode('unicode-escape')
    print(unicode_2)
    print(type(unicode_2))

# Вариант 4 "облегченный вариант 3"

word_list_5 = ['разработка', 'сокет', 'декоратор']
for word in word_list_5:
    words = word.encode('unicode-escape').decode('utf-8')  # Получение строковых значений юникод точек
    unicode__ = words.encode('utf-8').decode('unicode-escape')
    print(unicode__)
    print(type(unicode__))












