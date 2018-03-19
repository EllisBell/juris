import trib_scraper as ts
import acordao_scraper as acs
import acordao_saver
import time

default_trib_dict = {
    "TRL": "/jtrl.nsf?OpenDatabase",
    "TRP": "/jtrp.nsf?OpenDatabase",
    "TRC": "/jtrc.nsf?OpenDatabase",
    "TRE": "/jtre.nsf?OpenDatabase",
    "TRG": "/jtrg.nsf?OpenDatabase"
}

start_time = None


def scrape_tribs(tribs = default_trib_dict, time_limit=None):
    start_time = time.time()
    for trib_id, url in tribs.items():
        scrape_and_save_all(url, trib_id, time_limit)


# for scraping and saving everything unsaved
# call this for each trib you want to scrape
# trib_url is something like "/jtrl.nsf?OpenDatabase"
def scrape_and_save_all(trib_url, trib_id, time_limit=None):
    # Should we pass count to scrape_and_save or just pass -1 by default to scrape_trib - to get everything?
    # Probably have another method which calls this passing in -1
    all_urls = ts.scrape_all(trib_url)
    save_acordaos(all_urls, trib_id, time_limit)


def scrape_and_save_exact(trib_url, trib_id, count, start):
    all_urls = ts.scrape_exact_amount(trib_url, count, start)
    save_acordaos(all_urls, trib_id)


def save_acordaos(acordao_urls, trib_id, time_limit=None):
    ac_saver = acordao_saver.AcordaoSaver()
    currently_saved = ac_saver.get_currently_saved(trib_id)

    unsaved_urls = [url for url in acordao_urls if url not in currently_saved]
    for url in unsaved_urls:
        if time_limit and ((time.time() - start_time) > time_limit):
            break
        ac = acs.get_acordao(url, trib_id)
        if ac:
            ac_saver.save(ac)
            print("saved " + ac.processo)

    # TODO deal with this connection stuff
    ac_saver.close_connection()
