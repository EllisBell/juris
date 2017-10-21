import trib_scraper as ts
import acordao_scraper as acs
import acordao_saver


# for scraping and saving everything unsaved
# call this for each trib you want to scrape
def scrape_and_save(trib_url, trib_id):
    all_urls = ts.scrape_trib(trib_url, count=10)

    ac_saver = acordao_saver.AcordaoSaver()
    currently_saved = ac_saver.get_currently_saved(trib_id)

    unsaved_urls = [url for url in all_urls if url not in currently_saved]
    for url in unsaved_urls:
        ac = acs.get_acordao(url, trib_id)
        ac_saver.save(ac)

    ac_saver.close_connection()
