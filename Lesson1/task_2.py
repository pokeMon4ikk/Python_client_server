"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

word_list = []

word_list.append(b'class')
word_list.append(b'function')
word_list.append(b'method')

for word in word_list:
    print(word)
    print(type(word))
    print(len(word))





