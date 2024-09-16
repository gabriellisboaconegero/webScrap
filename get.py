#! /home/gabriel/webScrap/myenv/bin/python
from bs4 import BeautifulSoup
import requests

search = 'wikipedia'
url = 'https://www.google.com/search'

headers = {
	'Accept' : '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
}
parameters = {'q': search}

content = requests.get(url, headers = headers, params = parameters).text
soup = BeautifulSoup(content, 'html.parser')
print(soup)
exit(0)

search = soup.find(id = 'search')
links = search.find_all('a')
for link in links:
    print(link['href'])

