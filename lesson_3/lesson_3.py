from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pprint import pprint


# Создаю инициализацию к серверу MongoDB. Это мост,
# который является связью между приложением и базой данных
# в качестве параметров указываю ip адресс и порт
client = MongoClient('127.0.0.1', 27017)

# Создаю указатель на базу данных. В скобках указываю название базы данных
# Если база данных существует - она выберется, если нет - то указатель
# будет указывать на базу, которая в дальнейшем создастся (в ходе моей работы)
db = client['users']

# создаю указатели на коллекию persons в БД db
persons = db.persons
books = db.books

#CREATE

doc = {'_id': 123456789,
        "author": "Peter2",
        "age": 38,
        "text": "is cool! Wildberry",
        "tags": ['cool', 'hot', 'ice'],
        "date": '14.06.1983'}
#
# # Вставляю данные из словаря в раннее созданную коллекцию
# # Также делаю проверку на то, что документ с таким id уже существует
# # Вначале запустил код, не указывая вручную _id документа,
# # потом запустил код, указав. Поэтому в итоге получится их 2
try:
    persons.insert_one(doc)
except DuplicateKeyError:
    print(f"Document with id = {doc['_id']} already exists")

# insert_many нежелательный запрос, поскольку, если будет ошибка с Anna,
# то John вставится, а Anna и Jane нет
persons.insert_many([{"author": "John",
                "age" : 29,
                "text": "Too bad! Strawberry",
                "tags": 'ice',
                "date": '04.08.1971'},

                {"_id": 123,
                "author": "Anna",
                "age" : 36,
                "title": "Hot Cool!!!",
                "text": "easy too!",
                "date": '26.01.1995'},

                {"author": "Jane",
                "age" : 43,
                "title": "Nice book",
                "text": "Pretty text not long",
                "date": '08.08.1975',
                "tags":['fantastic', 'criminal']}])


# Делаю запрос, который извлекает все документы из коллекции
# # При повторном запуске кода в бд добавится такой же документ и их станет 2
for doc in persons.find({}):
    pprint(doc)

# READ
#
# Вывести все содержимое всех документов в коллекции
for doc in persons.find({}):
    pprint(doc)
#
# Найти только те докуметы, у которых автором является Peter2
for doc in persons.find({'author': 'Peter2'}):
    pprint(doc)
#
# Поиск по нескольким параметрам, ставится логическое &
for doc in persons.find({'author': 'Peter2', 'age': 38}):
    pprint(doc)
#
# Поиск с логическим или
for doc in persons.find({'$or': [{'author': 'Peter2'}, {'age': 29}]}):
    pprint(doc)
#
# Вывести только те документы, в которых значение ключа age >=30,
# чтобы вывести значения <=30, пишу lte (e=equal)
for doc in persons.find({'age': {'$gte': 30}}):
    pprint(doc)
#
# Поиск документов, у которых имя Питер или возраст <=30
for doc in persons.find({'$or': [{'author': 'Peter2'}, {'age': {'$lte': 30}}]}):
    pprint(doc)


# UPDATE

new_data = {"author": "Andrey",
         "age" : 28,
         "text": "is hot!",
         "date": '11.09.1991'}

# Заменяю значение ключа age в документе, где параметр author = Peter2 на 39
# Заменится первый попавшийся документ, который соответствует критериям
# Чтобы поменять несколько полей - в словаре с age, указать ещё одно ключ-значение
persons.update_one({'author': 'Peter2'}, {'$set': {'age': 39}})
#
# Заменить первый попавшийся документ, который соответствует параметрам поиска
# на новый словарь (документ). Заменится не просто имя, а весь документ,
# кроме поля tags, посколько его в словаре new_data не было
# update_many обновит не первый попавшийся документ, а все, которые соответствуют поиску
persons.update_one({'author': 'Peter2'}, {'$set': new_data})
#
# Решаю задачу с тем, что осталось поле tags, применив метод replace
# Данный метод полностью заменяет один документ на другой
# replace_many заменит не первый попавшийся документ, а все, которые соответствуют поиску
persons.replace_one({'author': 'Andrey'}, new_data)
#
#
# DELETE
# Удалить первый попавшийся документ, который соответствует параментрам поиска
# many удалит все документы по указанному параметру
persons.delete_one({'author': 'Peter2'})
#
# Удалить только одно поле (ключ-значение) у одного документа
persons.update_one({'author': 'John'}, {'$unset': {'date': False}})
#
# Удалить все документы
persons.delete_many({})

for doc in persons.find({}):
    pprint(doc)


