from . import search as s
from datetime import datetime
from .models import SearchHistory
from django.utils import timezone


class AcordaoSearchData:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


# interface
# Main search, called from view
# def get_search_results(query, tribs, page, display, sort_by):
#     if query[0] == "\"" and query[-1] == "\"":
#         query = query.replace("\"", "")
#         results = phrase_search(query, tribs, page, display, sort_by)
#     elif ' ou ' in query.lower():
#         query = query.replace(" ou ", " ")
#         results = or_search(query, tribs, page, display, sort_by)
#     else:
#         results = and_search(query, tribs, page, display, sort_by)
#
#     return results

def get_search_results(asd, display, sort_by):
    if asd.query[0] == "\"" and asd.query[-1] == "\"":
        asd.query = asd.query.replace("\"", "")
        results = phrase_search(asd, display, sort_by)
    elif ' ou ' in asd.query.lower():
        asd.query = asd.query.replace(" ou ", " ")
        results = or_search(asd, display, sort_by)
    else:
        results = and_search(asd, display, sort_by)

    return results


def and_search(asd, display_size, sort_by=None):
    return search_with_paging(asd, "and", display_size, sort_by)


def or_search(asd, display_size, sort_by=None):
    return search_with_paging(asd, "or", display_size, sort_by)


def phrase_search(asd, display_size, sort_by=None):
    return search_with_paging(asd, "and", display_size, sort_by, "phrase")


def search_with_paging(asd, operator, display_size, sort_by, query_type="most_fields"):
    if not asd.page_number:
        asd.page_number = 1

    # field to filter on and values to filter for
    filter_dict = {"tribunal": asd.tribs}

    start = (asd.page_number - 1) * display_size
    exclude = ['tribunal', 'txt_integral', 'txt_parcial']

    sd = s.SearchData(index='acordao_idx', query=asd.query, searchable_fields=get_searchable_fields(),
                      match_type=query_type, operator=operator, sort_by=sort_by, filter_dict=filter_dict,
                      exclude=exclude, start_at=start, res_size=display_size)

    res = s.search_fields(sd)

    results = get_results_dict_from_res(res)
    results = format_dates(results)
    results = add_paging_info(results, asd.page_number, display_size)
    return results


def get_searchable_fields():
    # ^ syntax weights fields more
    return ["processo^2", "relator^2", "sumario", "txt_integral", "txt_parcial", "descritores^2"]


def get_ids_from_res(res):
    res_data = res['hits']['hits']
    ac_ids = [hit["_id"] for hit in res_data]
    return ac_ids


def get_results_dict_from_res(res):
    results = {}
    results['total'] = res['hits']['total']
    results['acordaos'] = [d['_source'] for d in res['hits']['hits']]

    # for acordao in results['acordaos']:
    #    acordao['data'] = datetime.strptime(acordao['data'], "%Y-%m-%d")

    return results


def format_dates(results):
    for acordao in results['acordaos']:
        acordao['data'] = datetime.strptime(acordao['data'], "%Y-%m-%d")
    return results


def add_paging_info(results, page_number, display_size):
    total = results['total']
    has_next = (page_number * display_size) < total
    has_previous = (page_number is not 1) and (page_number - 1) * display_size < total
    results['has_next'] = has_next
    results['has_previous'] = has_previous

    return results


def save_search(query):
    sh = SearchHistory()
    sh.term = query
    sh.date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    sh.save()
