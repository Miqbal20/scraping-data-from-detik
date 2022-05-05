import os
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

# Definisi Parameter
url = 'https://www.detik.com/search/searchall?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
           '(KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}


def get_total_pages(query):
    params = {
        'query': query,
        'siteid': '2',
    }

    res = requests.get(url, params=params, headers=headers)

    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('div', 'paging text_center')
    pages = pagination.findAll('a')
    total_pages = []
    for page in pages:
        total_pages.append(page.text)
    total = int(max(total_pages))
    return total


def get_all_item(query, pages):
    params = {
        'query': query,
        'siteid': '2',
        'page': pages,
    }
    res = requests.get(url, params=params, headers=headers)

    # proses Scraping
    soup = BeautifulSoup(res.text, 'html.parser')
    contents = soup.find('div', 'list-berita')
    article = contents.findAll('article')
    newslist = []
    for item in article:
        title = item.find('h2', 'title').text
        link = item.find('a')['href']
        desc = item.find('p').text
        getdate = item.find('span', 'date')
        tag = getdate.text.split(', ')[0]
        date = getdate.text.split(', ')[1]

        data_dict = {
            'judul': title,
            'url': link,
            'deskripsi': desc,
            'tag': tag,
            'tanggal': date,
        }
        newslist.append(data_dict)

    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    # export ke json
    with open(f'json_result/{query}_in_page_{pages}.json', 'w+') as json_data:
        json.dump(newslist, json_data)
    print(f'json page {pages} berhasil dibuat')
    return newslist


def create_document(data_frame, file_name, pages):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    # export ke csv & excel
    df = pd.DataFrame(data_frame)
    df.to_csv(f'data_result/{file_name}.csv', index=False)
    print(f'Data {file_name} di page {pages} berhasil di Export ke Csv')
    df.to_excel(f'data_result/{file_name}.xlsx', index=False)
    print(f'Data {file_name} di page {pages} berhasil di Export ke Excel')


def run():
    query = input('Masukan kata kunci: ')
    total = get_total_pages(query)
    final_result = []
    for pages in range(total):
        pages += 1
        final_result += get_all_item(query, pages)

        # formating data
        try:
            os.mkdir('reports')
        except FileExistsError:
            pass

        with open('reports/{}.json'.format(query), 'w+') as final_data:
            json.dump(final_result, final_data)

        print('Report Json berhasil dibuat\n')
        create_document(final_result, query, pages)


if __name__ == '__main__':
    run()
