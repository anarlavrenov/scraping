# Это класс, объект которого создавать не буду. Он будет создан автоматически при запуске приложения
# name - указывается название паука
# allowed_domains - на какие домены паук может ходить. Если нужно несколько, то через запятую нужно указать их
# start_urls - позволяет задать несколько точек входа. Удалил изначальный - djinni.co.
    # - Поставил первую ссылку на вакансию Python и регионом: Украина
    # - Поставил вторую ссылку на вакансию Python и регионом: Страны ЕС
    # Указывая ссылки в start_urls подразумеваю, что при выполнении приложения автоматически будет get запросы
    # по каждой ссылок, указанной в этом списке. Придет response и он упадет в параметр метода parse(ниже)
    # При том метод parse я тоже вызывать не буду, он вызовется автоматически и сам примет response
# Чтобы запускать код не через терминал (чтобы делать дебаг), создаю файл runner.py

import scrapy
# Импортирую класс HtmlResponse и вставляю его рядом с response в параметрах метода parse,
# чтобы при вызове response появлялись подсказки
from scrapy.http import HtmlResponse
# Импортирую класс JobparserItem, чтобы можно было его создать и вернуть
from jobparser.items import JobparserItem



class DjinnicoSpider(scrapy.Spider):
    name = 'djinnico'
    allowed_domains = ['djinni.co']
    start_urls = ['https://djinni.co/jobs/?keywords=python&region=ukraine',
                  'https://djinni.co/jobs/?keywords=python&region=eu']


    def parse(self, response: HtmlResponse):
        # Прописываю логику перехода на следующую страницу.
        # get() возвратит всегда первый найденный элемент (ссылку, не объект)
        # (даже если их несколько соответствуют параметрам)
        next_page = response.xpath("//a[contains(text(), 'наступна')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        # Собираю ссылки на вакансии. Чтобы получить не объекты, а данные - нужно применить метод getall
        # Получил относительные ссылки
        links_raw = response.xpath("//a[@class='profile']/@href").getall()
        # Циклом ниже делаю стандартную прогонку по относительным ссылкам и делаю из них абсолютные (для работы)
        # Сохраняю полученный результат в список links
        links = []
        for el in links_raw:
            el = 'https://djinni.co' + el
            links.append(el)
        # Пишу цикл для перехода внутрь каждой ссылки.
        # Чтобы сделать запрос в текущем (scrapy) response, нужно вызвать метод follow() и callback
        # для асинхронных запросов
        # Мне нужно вернуть результат выполнения get запроса в новый метод(callback функцию), для этого использую yield
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
    # Создаю функцию для callback. В данный response будет заходить ответ от каждой ссылки
    # Тут уже и собираю все данные
    def vacancy_parse(self, response: HtmlResponse):
        # Имя вакансии
        name = response.xpath("//div[@class='job-post--title-wrapper']/h1/text()").get()
        # Зарплата (необработанная)
        salary = response.xpath("//h1/span[@class='public-salary-item']/text()").get()
        # Ссылка на вакансию
        url = response.url
        # Должен вернуть экземпляр класса items.py
        yield JobparserItem(name=name, salary=salary, url=url)
        # После проделанных всех операций осталось данные обработать
        # Это делается в отдельном файле pipelines.py и его классе JobparserPipeline
        # Стоял брейкпоинт на yield, убрал его и поставил на print в pipelines.py для проведения дебага через runner.py


        # Вывожу ссылки от запроса на два url (starts_url). Закомментировал, в процессе работы уже не актуально
        # print(response.url)

