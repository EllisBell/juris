from collections import OrderedDict
import trib_scraper as ts
import acordao_scraper as acs
import acordao_saver
import time

default_trib_dict = OrderedDict([
    ("TRL", "/jtrl.nsf?OpenDatabase"),
    ("TRP", "/jtrp.nsf?OpenDatabase"),
    ("TRC", "/jtrc.nsf?OpenDatabase"),
    ("TRE", "/jtre.nsf?OpenDatabase"),
    ("TRG", "/jtrg.nsf?OpenDatabase"),
    ("STJ", "/jstj.nsf?OpenDatabase")
])


def scrape_tribs(tribs=default_trib_dict, time_limit=None):
    start_time = time.time()
    all_errors = []
    for trib_id, url in tribs.items():
        print("SCRAPING " + trib_id)
        errors = scrape_and_save_all(url, trib_id, start_time, time_limit)
        all_errors.extend(errors)
    print("FINISHED SCRAPING")
    return all_errors


# for scraping and saving everything unsaved
# call this for each trib you want to scrape
# trib_url is something like "/jtrl.nsf?OpenDatabase"
def scrape_and_save_all(trib_url, trib_id, start_time, time_limit=None):
    # Should we pass count to scrape_and_save or just pass -1 by default to scrape_trib - to get everything?
    # Probably have another method which calls this passing in -1
    all_urls = ts.scrape_all(trib_url)
    errors = save_acordaos(all_urls, trib_id, start_time, time_limit)
    return errors


def scrape_and_save_exact(trib_url, trib_id, count, start):
    all_urls = ts.scrape_exact_amount(trib_url, count, start)
    errors = save_acordaos(all_urls, trib_id, None)


def save_acordaos(acordao_urls, trib_id, start_time, time_limit=None):
    ac_saver = acordao_saver.AcordaoSaver()
    currently_saved = ac_saver.get_currently_saved(trib_id)

    unsaved_urls = [url for url in acordao_urls if url not in currently_saved]
    bad_urls = []
    for url in unsaved_urls:
        try:
            if time_limit and ((time.time() - start_time) > time_limit):
                print("IT HAS BEEN TOO LONG")
                break
            ac = acs.get_acordao(url, trib_id)
            if ac:
                ac_saver.save(ac)
        except Exception as e:
            bad_urls.append(url)

    # TODO deal with this connection stuff
    ac_saver.close_connection()
    return bad_urls


def get_newly_saved():
    ac_saver = acordao_saver.AcordaoSaver()
    new = ac_saver.get_saved_since(12)
    ac_saver.close_connection()
    return new


def delete_deprecated_dups(time_limit=None):
    start_time = time.time()
    ac_saver = acordao_saver.AcordaoSaver()
    dups = ac_saver.get_duplicate_processos()
    print("CHECKING DUPS")
    for url in dups:
        time.sleep(0.2)
        if time_limit and ((time.time() - start_time) > time_limit):
            print("CHECKING DUPS HAS TAKEN TOO LONG")
            break
        if acs.check_source_not_found(url):
            ac_saver.delete_acordao_by_url(url)
            print("not found: " + url)

    ac_saver.close_connection()
