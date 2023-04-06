import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup, quotes):
    # получение всех элементов <div> с классом "quote" на странице
    quote_elements = soup.find_all('div', class_='quote')

    # перебор списка элементов цитат для извлечения интересующих данных и сохранения их в списке "quotes"
    for quote_element in quote_elements:
        # извлечение текста цитаты
        text = quote_element.find('span', class_='text').text
        # извлечение автора цитаты
        author = quote_element.find('small', class_='author').text

        # получение элементов <a> связанных с тегами цитаты
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        # сохранение списка тегов в списке
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        # добавление словаря с данными цитаты в список "quotes"
        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)  # объединение тегов в строку "A, B, ..., Z"
            }
        )

# URL домашней страницы целевого сайта
base_url = 'https://quotes.toscrape.com'

# заголовок User-Agent для использования в GET-запросе ниже
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# получение целевой веб-страницы
page = requests.get(base_url, headers=headers)

# парсинг целевой веб-страницы с помощью Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# инициализация переменной, которая будет содержать список всех данных цитат
quotes = []

# скрапинг домашней страницы
scrape_page(soup, quotes)

# получение HTML-элемента "Next →"
next_li_element = soup.find('li', class_='next')

# если есть следующая страница для скрапинга
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # получение новой страницы
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # парсинг новой страницы
    soup = BeautifulSoup(page.text, 'html.parser')

    # скрапинг новой страницы
    scrape_page(soup, quotes)

    # поиск HTML-элемента "Next →" на новой странице
    next_li_element = soup.find('li', class_='next')

# чтение файла "quotes.csv" и создание его, если он отсутствует
csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

# инициализация объекта записи для вставки данных в файл CSV
writer = csv.writer(csv_file)

# запись заголовка файла CSV
writer.writerow(['Text', 'Author', 'Tags'])

# запись каждой строки в файл CSV
for quote in quotes:
    writer.writerow(quote.values())

# завершение операции и освобождение ресурсов
csv_file.close()
