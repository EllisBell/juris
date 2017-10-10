import requests
from bs4 import BeautifulSoup
import re
import acordao_scraper as acs

headers = {'User-Agent': 'Mozilla/5.0'}

base_url = 'http://www.dgsi.pt'


def scrape_page(page_url):
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Get links for the acordaos
    links = soup.find_all('a', href=re.compile('OpenDocument'))
    acordaos = []
    for link in links:
        ac = acs.get_acordao(base_url + link['href'])
        acordaos.append(ac)

    return acordaos

