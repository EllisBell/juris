import scraper
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'http://www.dgsi.pt'
max_page_count = 1000


# Return how many acordaos scraped
# Here just scrape for acordao urls
def scrape_page(page_url):
    content = scraper.try_get_page_content(page_url, 5, 1)
    soup = BeautifulSoup(content, 'html.parser')
    # Get links for the acordaos
    links = soup.find_all('a', href=re.compile('OpenDocument'))
    acordao_urls = [link['href'] for link in links]

    return acordao_urls


# It is possible that new acordaos are added and displayed after acordaos we have already
# scraped. Therefore we can't stop at the first already scraped acordao as we don't know
# whether there will be unscraped ones that have been added. So might have to scrape
# the whole thing every time.

# To speed this up a bit, display maximum number of acordaos on page (looks like it's 1000)
def scrape_all(trib_url):
    base_trib_url = base_url + trib_url
    all_acordao_urls = []
    start_index = 1

    while True:
        # get links to acordaos from page
        acordao_urls = scrape_page(base_trib_url + "&Start=" + str(start_index) + "&Count=" + str(max_page_count))
        # check if got anything back
        if not acordao_urls:
            break

        all_acordao_urls.extend(acordao_urls)
        # subtract the number of acordaos we just got from the remaining count
        start_index = start_index + len(acordao_urls)

    return all_acordao_urls


def scrape_exact_amount(trib_url, num_to_scrape, start_index=1):
    base_trib_url = base_url + trib_url
    all_acordao_urls = []
    remaining_count = num_to_scrape

    while remaining_count > 0:
        # get links to acordaos from page
        acordao_urls = scrape_page(base_trib_url + "&Start=" + str(start_index) + "&Count=" + str(max_page_count))
        # check if got anything back
        if not acordao_urls:
            break

        # if remaining count smaller than number we actually got, cut to that
        if remaining_count < len(acordao_urls):
            acordao_urls = acordao_urls[:remaining_count]

        all_acordao_urls.extend(acordao_urls)
        # subtract the number of acordaos we just got from the remaining count
        remaining_count = remaining_count - len(acordao_urls)
        start_index = start_index + len(acordao_urls)

    return all_acordao_urls

    #
    # def placeholder_save():
    #     unsaved = [ac_url for ac_url in acordao_urls if ac_url not in currently_saved]
    #
    #     # Here make call to database to get acordaos currently in DB
    #     # Whatever is not there, call acs.get_acordao and then save to db
    #     ac_saver = acordao_saver.AcordaoSaver()
    #     currently_saved = ac_saver.get_currently_saved(trib_id)
