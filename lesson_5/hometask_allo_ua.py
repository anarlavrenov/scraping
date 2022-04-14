from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from hashlib import md5


# БД
client = MongoClient('127.0.0.1', 27017)
db = client['goods']
goods = db.goods

# Функция для создания хеша внутри документа в БД
def hash_id(doc):
    bytes_input = str(doc).encode('utf-8')

    return md5(bytes_input).hexdigest()

s = Service('./chromedriver.exe')
options = Options()
options.add_argument('start-maximized')
# Убираю всплывающие окна
options.add_argument('--disable-notifications')
driver = webdriver.Chrome(service=s, options=options)

# Перехожу на сайт Алиэкспресс
driver.get('https://allo.ua/')

# Скроллюсь да блока с Новинками
title = driver.find_element(By.XPATH, "//div[@data-products-type='hot']/h2[@class='h-products__title']")
actions = ActionChains(driver)
actions.move_to_element(title)
actions.perform()

# Переключаюсь на тег 'Аудио'
driver.find_element(By.XPATH, "//div[@class='home-promo-news']/../div[@data-products-type='hot']//a[@class='v-pt__link' and @data-tab-id='5269']").click()

# Нажимаю на кнопку 'Показать ещё', чтобы вывести полный список товаров по тегу 'Аудио'
while True:
    try:
        wait = WebDriverWait(driver, 15)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='home-promo-news']/../div[@data-products-type='hot']//button[@class='h-pl__more-button']")))
        button.click()
    except exceptions.TimeoutException:
        break

# Ссылки на товары
goods_links_selenium = driver.find_elements(By.XPATH, "//div[@class='home-promo-news']/../div[@data-products-type='hot']//div[@class='h-pc no-rect-labels']//a[@class='product-card__title h-pc__title']")

goods_links = []

for link in goods_links_selenium:
    elem = link.get_attribute('href')
    goods_links.append(elem)

goods_list = []

for elem in goods_links:
    goods_data = {}
    driver.get(elem)

    good_name = driver.find_element(By.XPATH, "//h1[@class='p-view__header-title']").text

    try:
        good_price = driver.find_element(By.XPATH, "//div[@class='p-trade-price__current']//span[@class='sum']").text
        good_price = int(good_price.rpartition('₴')[0].replace(' ', ''))

    except exceptions.NoSuchElementException:
        good_price = driver.find_element(By.XPATH, "//div[@class='p-trade-price__current p-trade-price__current--discount']//span[@class='sum']").text
        good_price = int(good_price.rpartition('₴')[0].replace(' ', ''))

    try:
        good_rating = driver.find_element(By.XPATH, "//span[@class='rating-block__stars-count']").text
        good_rating = float(good_rating)

    except exceptions.NoSuchElementException:
        good_rating = None

    goods_data['name'] = good_name
    goods_data['price'] = good_price
    goods_data['link'] = elem
    goods_data['rating'] = good_rating

    _id = hash_id(goods_data)
    goods_data['_id'] = _id

    goods_list.append(goods_data)

    try:
        goods.insert_one(goods_data)
    except DuplicateKeyError:
        pass


for doc in goods.find({}):
    pprint(doc)

total_count = goods.count_documents({})
print(total_count)