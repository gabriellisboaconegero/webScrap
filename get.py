#! /usr/bin/env python
# ================== USE CONDA ==================
from bs4 import BeautifulSoup
import requests
import argparse

parser = argparse.ArgumentParser(description='Faz um web scrapping')
parser.add_argument(
    '--dump-html',
    dest='dump_html',
    action='store_true',
    help='Se deve jogar o html da página pega'
)
args = parser.parse_args()

SEARCH = 'new rtx 5000 series'
URL = 'https://www.google.com/search'

HEADERS = {
	'Accept' : '*/*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': SEARCH}

if __name__ == "__main__":
    req1 = requests.get(URL, headers = HEADERS, params = parameters)
    # Sai se requesição não for 200 (OK)
    req1.raise_for_status()
    soup = BeautifulSoup(req1.text, 'html.parser')
    # Se deve dumpar a pagina html
    if (args.dump_html):
        print(soup)
        exit(0)

    search = soup.find(id='search')
    links = search.find_all('a')
    # for link in links:
    #     print(link['href'])

    # Pega html do primeiro item da pesquisa
    req2 = requests.get(links[0]["href"])
    # Sai se requesição não for 200 (OK)
    req2.raise_for_status()
    soup = BeautifulSoup(req2.text, 'html.parser')

    print(soup)
