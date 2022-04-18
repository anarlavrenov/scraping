import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class WorkuaSpider(scrapy.Spider):
    name = 'workua'
    allowed_domains = ['work.ua']
    start_urls = ['https://www.work.ua/jobs-kyiv-manager/',
                  'https://www.work.ua/jobs-lviv-manager/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(text(), 'Наступна')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links_raw = response.xpath("//h2[@class='']/a/@href").getall()

        links = []
        for el in links_raw:
            el = 'https://www.work.ua' + el
            links.append(el)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        # Имя вакансии
        name = response.xpath("//h1[@id = 'h1-name']//text()").get()
        # Зарплата (необработанная)
        salary = response.xpath("//b[@class='text-black']/text()").get()
        # Ссылка на вакансию
        url = response.url

        yield JobparserItem(name=name, salary=salary, url=url)

