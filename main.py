import requests
from bs4 import BeautifulSoup
import json


# Функция для получения HTML-кода страницы
def get_page_html(url):
    response = requests.get(url)
    return response.text


# Функция для парсинга страницы и поиска вакансий
def parse_vacancies(url):
    html = get_page_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    vacancies = []

    # Находим все блоки с информацией о вакансиях
    vacancy_blocks = soup.find_all('div', class_='vacancy-block')

    for block in vacancy_blocks:
        # Получаем информацию о вакансии
        title = block.find('h2', class_='vacancy-title').text
        company = block.find('p', class_='vacancy-company').text
        city = block.find('p', class_='vacancy-city').text
        salary_range = block.find('p', class_='vacancy-salary').text
        link = block.find('a', class_='vacancy-link')['href']

        # Проверяем, содержит ли описание вакансии ключевые слова "Django" и "Flask"
        description = block.find('div', class_='vacancy-description').text
        if 'Django' in description and 'Flask' in description:
            vacancy_info = {
                'title': title,
                'company': company,
                'city': city,
                'salary_range': salary_range,
                'link': link
            }
            vacancies.append(vacancy_info)

    # Записываем информацию о вакансиях в JSON
    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(vacancies, f, ensure_ascii=False, indent=4)


# URL страницы со свежими вакансиями
url = 'https://example.com/vacancies?search=Python&city=Москва+Санкт-Петербург'

# Вызываем функцию для парсинга страницы и поиска вакансий
parse_vacancies(url)