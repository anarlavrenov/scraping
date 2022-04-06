import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

base_url = 'https://djinni.co'
url = base_url + '/jobs/?keywords=data+scientist'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

response = requests.get(url, headers=headers)

# with open('response.html', 'w', encoding='utf-8') as f:
#     f.write(response.text)

html_file = ''
with open('response.html', 'r', encoding='utf-8') as f:
    html_file = f.read()

dom = bs(html_file, 'html.parser')

vacancies = dom.find_all('li', {'class': 'list-jobs__item'})

vacancy_list = []

for vacancy in vacancies:
    vacancy_data = {}
    for span in vacancy.find('a', {'class': 'profile'}).findChildren():
        vacancy_name = span.text
    vacancy_link = base_url + vacancy.find('a', {'class': 'profile'})['href']
    site_name = dom.find('a', {'class': 'navbar-brand'}).getText()

    min_salary = vacancy.find('span', {'class': 'public-salary-item'})
    if min_salary:
        min_salary = min_salary.getText()
        if 'до' not in min_salary:
            min_salary = min_salary.rpartition('-')[0].strip('$')
            min_salary = int(min_salary)
        else:
            min_salary = None

    max_salary = vacancy.find('span', {'class': 'public-salary-item'})
    if max_salary:
        max_salary = max_salary.getText()
        if 'до' not in max_salary:
            max_salary = max_salary.split('-')[1]
        if 'до' in max_salary:
            max_salary = max_salary.split('до')[1].replace(' ', '').strip('$')
        max_salary = int(max_salary)
    else:
        max_salary = None

    currency = vacancy.find('span', {'class': 'public-salary-item'})
    if currency:
        currency = currency.getText()
        if '$' in currency:
            currency = 'usd'
    else:
        currency = None

    vacancy_data['name'] = vacancy_name
    vacancy_data['link'] = vacancy_link
    vacancy_data['site_name'] = site_name
    vacancy_data['min_salary'] = min_salary
    vacancy_data['max_salary'] = max_salary
    vacancy_data['currency'] = currency

    vacancy_list.append(vacancy_data)

pprint(vacancy_list)











