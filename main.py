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
        'query': 'crypto',
        'siteid': '2',
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    soup = BeautifulSoup(res.text, 'html.parser')
    pagination = soup.find('div', 'paging text_center')
    pages = pagination.findAll('a')
    total_pages = []
    for page in pages:
        total_pages.append(page.text)
    total = int(max(total_pages))
    return total


def get_all_item():
    params = {
        'query': 'crypto',
        'siteid': '2'
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
    with open(f'json_result/j.json', 'w+') as json_data:
        json.dump(newslist, json_data)
    print(f'json berhasil dibuat')
    return newslist

    # print(newslist)


if __name__ == '__main__':
    get_all_item()
