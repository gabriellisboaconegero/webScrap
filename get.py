#! /usr/bin/env python
# ================== USE CONDA ==================
from bs4 import BeautifulSoup
import requests

search = 'wikipedia grécia'
url = 'https://www.google.com/search'

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': search}

req1 = requests.get(url, headers = headers, params = parameters)
# Sai se requesição não for 200 (OK)
req1.raise_for_status()
soup = BeautifulSoup(req1.text, 'html.parser')

search = soup.find(id='search')
links = search.find_all('a')
# for link in links:
#     print(link['href'])

req2 = requests.get(links[0]["href"])
# Sai se requesição não for 200 (OK)
req2.raise_for_status()
soup = BeautifulSoup(req2.text, 'html.parser')

print(soup)
