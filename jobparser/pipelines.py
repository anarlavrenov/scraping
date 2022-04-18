# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.http import HtmlResponse
from hashlib import md5
import unicodedata
from html import unescape
import string

# БД
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class JobparserPipeline:
    # В параметр item придет сформированный объект item (после yield JobparserItem)
    # метод process_item будет сам, в нужный момент, вызван и сам примет item
    # Чтобы JobparserPipeline активировался, нужно перейти в settings.py и раскомментировать
    # три строчки ITEM_PIPELINES
    # Поставил брейкпоинт на print и вызвал дебаг через runner.py . В консоле прописал item - получил обьект на первую (потом убрал)
    # пришедшую вакансию
    # В этом классе совершается вся обработка данных

    # Подключение MongoDB
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        # создание бд
        self.mongobase = client.vacancies

    def process_item(self, item, spider):

        # В определенные поля item записал результат обработки через process_salary, в которую передаю грязную зарплату
        if spider.name == 'djinnico':
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_djinnico(item['salary'])
            item['name'] = self.process_name(item['name'])
            item['_id'] = self.hash_id(item)
        # и когда обработка произошла, можно удалить грязную зарплату из объекта вызовов items
            del item['salary']
        else:
            item['min_salary'], item['max_salary'], item['currency'] = self.process_salary_workua(item['salary'])
            item['_id'] = self.hash_id(item)
            del item['salary']


        # Создание коллекции
        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass

        return item
    # Метод, в котором нужно совершить обработку зарпалаты на мин, макс и валюту
    # Обработка зарплаты djinnico
    def process_salary_djinnico(self, salary):
        min_salary = salary
        if min_salary:
            if 'до' not in min_salary and '-' in min_salary:
                min_salary = int(min_salary.rpartition('-')[0].replace('$', ''))
            elif 'до' not in min_salary and '-' not in min_salary and 'від' not in min_salary:
                min_salary = int(min_salary.replace('$', ''))
            elif 'від' in min_salary:
                min_salary = int(min_salary.split('від')[1].replace(' ', '').strip('$'))
            else:
                min_salary = None
        else:
            min_salary = None

        max_salary = salary
        if max_salary:
            if '-' in max_salary and 'до' not in max_salary:
                max_salary = int(max_salary.split('-')[1])
            elif 'до' in max_salary and '-' not in max_salary:
                max_salary = int(max_salary.split('до')[1].replace(' ', '').strip('$'))
            else:
                max_salary = None
        else:
            max_salary = None

        currency = salary
        if currency:
            if '$' in currency:
                currency = 'usd'
        else:
            currency = None

        return min_salary, max_salary, currency

    # Обработка имени вакансии для djinnico
    def process_name(self, name: HtmlResponse):
        if '\n' in name:
          name = name.replace('\n', '').strip()
        else:
            pass
        return name

    # Хеширование документов
    def hash_id(self, item):
        bytes_input = str(item).encode('utf-8')

        return md5(bytes_input).hexdigest()

    # Обработка зарплаты workua
    def process_salary_workua(self, salary):
        min_salary = salary
        if min_salary:
            min_salary = unescape(min_salary)
            min_salary = unicodedata.normalize('NFKC', min_salary)

            if '–' in min_salary:
                min_salary = int(min_salary.rpartition('–')[0].replace(' ', ''))
            elif '–' not in min_salary:
                min_salary = int(min_salary.replace('грн', '').replace(' ', ''))
            else:
                min_salary = None
        else:
            min_salary = None

        max_salary = salary
        if max_salary:
            max_salary = unescape(max_salary)
            max_salary = unicodedata.normalize('NFKC', max_salary)
            if '–' in max_salary:
                max_salary = int(max_salary.split('–')[1].strip('грн').strip().translate({ord(c): None for c in string.whitespace}))
            else:
                max_salary = None
        else:
            max_salary = None

        currency = salary
        if currency:
            if 'грн' in currency:
                currency = 'uah'
            else:
                currency = None
        else:
            currency = None
        return min_salary, max_salary, currency








