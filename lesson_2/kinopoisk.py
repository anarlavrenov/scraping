# https://www.kinopoisk.ru/lists/movies/popular-series/?b=series

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

base_url = 'https://www.kinopoisk.ru'
url = base_url + '/lists/movies/popular-series/?b=series'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

response = requests.get(url, headers=headers)
# Не создастся html файл. Полагаю, что связано это с тем,
# что российские сайты заблокированы в Украине
with open('response.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# Далее весь код нерабочий, посколько файла response.html у меня нет
html_file = ''
with open('response.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

dom = bs(html_file, 'html.parser')

serials = dom.find_all('div', {'class': 'styles_root__3a8vf'})

serial_list = []

for serial in serials:
    serial_data = {}
    # Получаю ссылку на фильм Постучись в мою дверь. Для этого нужно сделать дебаг на строке  31
    serial_link = base_url + serial.find_all('a', {'class': 'base-movie-main-info_link__3BnCh'})['href']
    # Получаю название фильма
    serial_name = serial.find('span', {'class': 'styles_mainTitle__3Bgao'}).getText()
    # Получаю информацию о сериале. На уроке в выводе в дебаге было xa0, поэтому также поставил пробел вместо этого
    serial_info = serial.find('span', {'class': 'desktop-list-main-info_truncatedText__2Q88H'}).getText().replace('\xa0', '')
    # Получаю рейтинг фильма
    serial_rating = serial.find('span', {'class': 'styles_kinopoiskValue__2oNdS'})
    # Делаю проверку, что если есть рейтинг у фильма, то из строки преобразовую рейтинг в флоат
    # Если рейтинга нет, то ставлю значение None
    if serial_rating:
        serial_rating = float(serial_rating.getText())
    else:
        serial_rating = None
    # В словарь записываю данные, полученные при цикле
    serial_data['link'] = serial_link
    serial_data['name'] = serial_name
    serial_data['info'] = serial_info
    serial_data['rating'] = serial_rating
    # Загоняю полученный словарь в список
    serial_list.append(serial_data)

pprint(serial_list)








