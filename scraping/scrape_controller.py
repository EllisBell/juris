import trib_scraper as ts
import acordao_scraper as acs
import acordao_saver
import time


# for scraping and saving everything unsaved
# call this for each trib you want to scrape
# trib_url is something like "/jtrl.nsf?OpenDatabase"
def scrape_and_save(trib_url, trib_id, count):
    # Should we pass count to scrape_and_save or just pass -1 by default to scrape_trib - to get everything?
    # Probably have another method which calls this passing in -1
    all_urls = ts.scrape_trib(trib_url, count=count)

    ac_saver = acordao_saver.AcordaoSaver()
    currently_saved = ac_saver.get_currently_saved(trib_id)

    unsaved_urls = [url for url in all_urls if url not in currently_saved]

    for url in unsaved_urls:
        time.sleep(0.8)
        ac = acs.get_acordao(url, trib_id)
        ac_saver.save(ac)
        print("saved " + ac.processo)

    ac_saver.close_connection()
