import requests
from bs4 import BeautifulSoup
import re
import acordao_scraper as acs

headers = {'User-Agent': 'Mozilla/5.0'}

base_url = 'http://www.dgsi.pt'


# Return how many acordaos scraped
# Here just scrape for acordao urls
def scrape_page(page_url):
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # Get links for the acordaos
    links = soup.find_all('a', href=re.compile('OpenDocument'))
    acordao_urls = [link['href'] for link in links]
    # acordaos = []
    # for link in links:
    #     ac = acs.get_acordao(base_url + link['href'])
    #     acordaos.append(ac)

    return acordao_urls



# It is possible that new acordaos are added and displayed after acordaos we have already
# scraped. Therefore we can't stop at the first already scraped acordao as we don't know
# whether there will be unscraped ones that have been added. So might have to scrape
# the whole thing every time.

# To speed this up a bit, display maximum number of acordaos on page (looks like it's 1000)
# Scrape just the links and check against urls in database. Then only scrape the ones we do
# not yet have in database
def scrape_trib(trib_url, start_index):
    base_trib_url = base_url + trib_url
    # keep going until you get to the end
    # display lots of acordaos (1000 seems to be max)
    while True:
        acordao_urls = scrape_page(base_trib_url + "&Start=" + start_index + "&Count=1000")
        # check if got anything back
        if not acordao_urls:
            break
        # Here make call to database to get acordaos currently in DB
        # Whatever is not there, call acs.get_acordao and then save to db
        with open("acordaos.txt", "a") as f:
            for ac in acordao_urls:
                f.write("\n" + ac.processo + "  " + ac.relator + "  " + ac.data)

        start_index = start_index + len(acordao_urls)

