import json

import requests

from bs4 import BeautifulSoup
from pprint import pprint
from fake_headers import Headers


def get_info(vacancy):
    title = vacancy.find('h3', attrs={'data-qa': 'bloko-header-3'}).text
    city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
    company = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
    salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary = salary.text if salary is not None else ''
    link = vacancy.find('a', attrs={'data-qa': 'serp-item__title'})['href']
    return {'title': title, 'city': city, 'company': company, 'salary': salary, 'link': link}

def check(vacancy):
    headers_gen = Headers(os='windows', browser='chrome')
    page = requests.get(vacancy['link'], headers=headers_gen.generate())
    soup = BeautifulSoup(page.text, 'html.parser')
    description = soup.find('div', attrs={'data-qa': 'vacancy-description'})
    return 'Django' in description.text or 'Flask' in description.text

if __name__ == '__main__':
    headers_gen = Headers(os='windows', browser='chrome')
    page = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=headers_gen.generate())
    soup = BeautifulSoup(page.text, 'html.parser')
    vacancies = soup.find_all('div', class_="vacancy-serp-item-body")
    vacancies_info = [get_info(vacancy) for vacancy in vacancies]
    vacancy_results = [vacancy for vacancy in vacancies_info if check(vacancy)]

    # Приведем текст в читаемый вид:
    for vacancy in vacancy_results:
        vacancy['company'] = vacancy['company'].replace('\xa0', ' ')
        vacancy['salary'] = vacancy['salary'].replace('\u202f', ' ')
        vacancy['city'] = vacancy['city'].replace('\xa0', ' ')
    # pprint(vacancy_results)


    with open('vacancy.json', 'w', encoding="utf-8") as file:
        json.dump(vacancy_results, file, indent=4, ensure_ascii=False)


