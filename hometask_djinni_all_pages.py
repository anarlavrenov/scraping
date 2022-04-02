import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import csv


page = 1
vacancy_list = []

while page != 6:
    base_url = 'https://djinni.co'
    url = base_url + f'/jobs/?keywords=data+scientist&page={page}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    response = requests.get(url, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('li', {'class': 'list-jobs__item'})

    for vacancy in vacancies:
        vacancy_data = {}
        for span in vacancy.find('a', {'class': 'profile'}).findChildren():
            vacancy_name = span.text
        vacancy_link = base_url + vacancy.find('a', {'class': 'profile'})['href']
        site_name = dom.find('a', {'class': 'navbar-brand'}).getText()

        min_salary = vacancy.find('span', {'class': 'public-salary-item'})
        if min_salary:
            min_salary = min_salary.getText()
            if 'до' not in min_salary and '-' in min_salary:
                min_salary = int(min_salary.rpartition('-')[0].replace('$', ''))
            elif 'до' not in min_salary and '-' not in min_salary:
                min_salary = int(min_salary.replace('$', ''))
            else:
                min_salary = None
        else:
            min_salary = None

        max_salary = vacancy.find('span', {'class': 'public-salary-item'})
        if max_salary:
            max_salary = max_salary.getText()
            if '-' in max_salary and 'до' not in max_salary:
                max_salary = int(max_salary.split('-')[1])
            elif 'до' in max_salary and '-' not in max_salary:
                max_salary = int(max_salary.split('до')[1].replace(' ', '').strip('$'))
            else:
                max_salary = None
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
    page = page + 1

pprint(vacancy_list)
pprint(len(vacancy_list))

with open('vacancies.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=vacancy_list[0].keys(),

                       )
    fc.writeheader()
    fc.writerows(vacancy_list)






















