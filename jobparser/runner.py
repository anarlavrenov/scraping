# Импортирую реактор, чтобы запускать несколько пауков одновременно
from twisted.internet import reactor
# Иипортирую запускальщик
from scrapy.crawler import CrawlerRunner
# Инициализирую процесс логирования
from scrapy.utils.log import configure_logging
# Импортирую метод с настройками проекта для моего паука(ов), чтобы он знал: с какими настройками работать
from scrapy.utils.project import get_project_settings

# Импортирую в настройки выше класс с текущим пауком (Djinni)
from jobparser.spiders.djinnico import DjinnicoSpider
# Импортирую в настройки выше класс с текущим пауком (Workua)
from jobparser.spiders.workua import WorkuaSpider

# Если импортировать файл runner, то код, который находится под if __name__ == '__main__' запускаться не будет
if __name__ == '__main__':
    # запускаю процесс логирования
    configure_logging()
    # Создаю настройки, запуская метод get_project_settings
    settings = get_project_settings()
    # Инициализирую запускальщика, передаю в параметры переменную settings строкой выше
    runner = CrawlerRunner(settings)
    # runner наделеяю классом, который должен работать
    # Первый паук
    runner.crawl(DjinnicoSpider)
    # Второй паук
    runner.crawl(WorkuaSpider)
    # Нужно для одновременной работы двух пауков
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # Запускаю реактор
    reactor.run()

# Теперь могу запускать дебаггер и смотреть, что не работает
# Для этого нужно ставить брейкпоинт в djinnico.py и запускать debug в runner.py
# Вначале обработается первая ссылка. Для того, чтобы получить вторую - нужно нажать Resume Program