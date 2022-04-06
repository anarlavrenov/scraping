import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

# Указываю url, через который буду парсить
url = 'https://google.com'

# Заношу в переменную html код полученной страницы
response = requests.get(url)

# Из сырого кода страницы формирую дом структуру. Для этого в параметрах
# передаю сырой код страницы(строка) и html.parser
dom = bs(response.text, 'html.parser')

# В полученном доме ишу первый попавшийся тег a
tag_a = dom.find('a')
pprint(tag_a)

# Нахожу родительский элемент тега a
parent_a = tag_a.parent
#pprint(parent_a)

# Через find_all можно вывести все элементы(в данном случае - теги),
# которые удовлетворяют поиск. И потом вывести нужный(по индексу)
tag_a_all = dom.find_all('a')
#pprint(tag_a_all[0])

# Нахожу всех детей parent_a(родителя tag_a).
# Для того, чтобы вернулся список детей, а не объект - делаю из полученного объекта список
# Считаются только теги
children_nobr = list(parent_a.children)
#pprint(children_nobr)
# Длина списка может быть больше, чем к-во детей,
# потому что считаются также и переносы строки
#pprint(len(children_nobr))

# Данный метод не учитывает переносы,
# Но считает и детей детей родителя (то есть вложенность)
children_nobr_2 = parent_a.findChildren()
#pprint(len(children_nobr_2))

# Вывожу детей без вложенности (решение проблемы children_nobr_2)
children_nobr_3 = parent_a.findChildren(recursive=False)
#pprint(len(children_nobr_3))

# Нахожу выбранный div по его id
div_SIvCob = dom.find('div', {'id': 'SIvCob'})
print(div_SIvCob)

# Нахожу выбранный div по его классу.
# Почему-то прилетает пустой список
# Все теги, в составе которых есть данный класс, должны быть возвращены
# Такое работает только с классами
div_o3j99 = dom.find_all('div', {'class': 'o3j99'})
pprint(div_o3j99)

# Нахожу div с двумя обязательными классами
# Для этого используются CSS селекторы
# Тоже возвращается пустой список
div_KxwPGc_AghGtd = dom.select('div.KxwPGc.AghGtd')
pprint(div_KxwPGc_AghGtd)

# Найти объект (не строку) по заданному тексту
# Вернется этот самый текст, но это будет не строка, а объект
# Для того, чтобы вывести тег с текстом, нужно написать pprint(text.search.parent)
# Возвращается None (не знаю: почему)
text_search = dom.find(text='Всё равно будет пустой список')
pprint(text_search)

