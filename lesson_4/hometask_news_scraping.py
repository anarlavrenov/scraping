from lxml import html
import requests
from pymongo import MongoClient
from pprint import pprint
# Буду делать уникальный id, точно также, как делал с вакансиями
from pymongo.errors import DuplicateKeyError

# БД
client = MongoClient('127.0.0.1', 27017)
db = client['media']
media = db.media

# XPath
url = 'https://hromadske.ua'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

# Скрапер

# Ссылки для 4 сабглавных новостей
news_links_raw = dom.xpath("//div[@class='MainBlock-cardWrapper']//a/@href")
news_links = []
for element in news_links_raw:
    element = url + element
    news_links.append(element)

# Сбор основной информации сабглавных новостей
news_list = []

for sub_news_item in news_links:

        news_data = {}
        url = sub_news_item
        response = requests.get(url, headers=header)
        dom = html.fromstring(response.text)

        news_name = dom.xpath("//h1[@class='PostHeader-title']/text()")
        news_date = dom.xpath("//div[@class='PostHeader-published']/text()")
        news_site = dom.xpath("//a[@class='HeaderMenu-logo']/@aria-label")

        news_data['name'] = news_name[0]
        news_data['date'] = news_date[0]
        news_data['site'] = news_site[0]
        news_data['link'] = sub_news_item

        news_list.append(news_data)


# Перевызываю переменные ниже для корретной работы приложения
url = 'https://hromadske.ua'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

# Ссылка на главную новость
main_news_link_raw = dom.xpath("//div[@class='MainBlock-postWrapper']//@href")
main_news_link = []
for element in main_news_link_raw:
    element = url + element
    main_news_link.append(element)

# Сбор основной информации главной новости
for main_news_item in main_news_link:
    main_news_data = {}
    url = main_news_item
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    main_news_name = dom.xpath("//h1[@class='PostHeader-title']/text()")
    main_news_date = dom.xpath("//div[@class='PostHeader-published']/text()")
    main_news_site = dom.xpath("//a[@class='HeaderMenu-logo']/@aria-label")


    main_news_data['link'] = main_news_item
    main_news_data['name'] = main_news_name[0]
    main_news_data['date'] = main_news_date[0]
    main_news_data['site'] = main_news_site[0]

    news_list.append(main_news_data)

# Добавляю уникальный id для словарей с новостями
news_id = 1

for element in news_list:
    element['_id'] = news_id
    news_id = news_id + 1

# Записываю данные в БД
try:
    for i in news_list:
        media.insert_one(i)
except DuplicateKeyError:
    pass

for doc in media.find({}):
    pprint(doc)

