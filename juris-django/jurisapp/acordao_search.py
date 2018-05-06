from . import search as s
from datetime import datetime
from dateutil import parser
from .models import SearchHistory
from django.utils import timezone
import shlex


class AcordaoSearchData:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        self.Phrases = None


# interface
# Main search, called from view
def get_search_results(asd, display, sort_by):
    results = []
    # for when there is no query but there is processo/dates
    if not asd.query:
        # results = and_search(asd, display, sort_by)
        results = search_with_paging(asd, display, sort_by)
    else:
        or_components = get_or_components(asd.query)
        results = search_with_paging(asd, display, sort_by, or_components)

    # elif is_valid_phrase_search(asd.query):
    #     res_dict = get_phrases(asd.query)
    #     normal_query = res_dict["normal"]
    #     phrase_list = res_dict["phrases"]
    #     asd.query = normal_query
    #     asd.Phrases = phrase_list
    #     results = phrase_search(asd, display, sort_by)
    # # TODO return some warning if unclosed quotes (odd number of quotes)
    # elif ' ou ' in asd.query.lower():
    #     asd.query = asd.query.replace(" ou ", " ")
    #     results = or_search(asd, display, sort_by)
    # else:
    #     results = and_search(asd, display, sort_by)

    return results


def get_or_components(query):
    or_parts = split_on_or(query)
    or_components = []
    for part in or_parts:
        component = get_or_component(part)
        or_components.append(component)

    return or_components


def split_on_or(query):
    or_parts = query.lower().split(" ou ")
    return or_parts


# get sublist for or_components
def get_or_component(or_part):
    or_component = []
    if is_valid_phrase_search(or_part):
        phrase_dict = get_phrases(or_part)
        for phrase in phrase_dict["phrases"]:
            or_dict = make_query_component(phrase, "phrase")
            or_component.append(or_dict)

        normal_part = phrase_dict["normal"]
        if normal_part:
            normal_dict = make_query_component(normal_part, "cross_fields")
            or_component.append(normal_dict)
    else:
        query_dict = make_query_component(or_part, "cross_fields")
        or_component.append(query_dict)

    return or_component


def make_query_component(query, type):
    return {"query": query, "type": type}


def is_valid_phrase_search(query):
    return query.count('"') > 0 and query.count('"') % 2 == 0


# todo only call this if even number of double quotes
def get_phrases(query):
    normal = ""
    phrases = []
    parts = shlex.split(query)
    for part in parts:
        # if longer than one word, it is a phrase
        if len(part.split()) > 1:
            phrases.append(part)
        else:
            normal = normal + " " + part

    normal = normal.strip()
    return {"normal": normal, "phrases": phrases}


# def and_search(asd, display_size, sort_by=None):
#     return search_with_paging(asd, "and", display_size, sort_by)
#
#
# def or_search(asd, display_size, sort_by=None):
#     return search_with_paging(asd, "or", display_size, sort_by)
#
#
# # TODO removing "phrase" query type argument
# def phrase_search(asd, display_size, sort_by=None):
#     return search_with_paging(asd, "and", display_size, sort_by)


# This is where we interact with elasticsearch
def search_with_paging(asd, display_size, sort_by, query_components=None):
    if not asd.page_number:
        asd.page_number = 1

    # field to filter on and values to filter for
    filter_dict = {"tribunal": asd.tribs}
    # add processo filter if there
    if asd.processo:
        filter_dict["processo.raw"] = [asd.processo, ]

    start = (asd.page_number - 1) * display_size
    exclude = ['tribunal', 'txt_integral', 'txt_parcial']

    sd = s.SearchData(index='acordao_idx', query=asd.query, from_date=asd.from_date,
                      to_date=asd.to_date, processo=asd.processo, searchable_fields=get_searchable_fields(),
                      sort_by=sort_by, filter_dict=filter_dict,
                      exclude=exclude, start_at=start, res_size=display_size, query_components=query_components)

    res = s.search_fields(sd)

    results = get_results_dict_from_res(res)
    results = format_dates(results)
    results = add_paging_info(results, asd.page_number, display_size)
    return results


def get_searchable_fields():
    # ^ syntax weights fields more
    return ["processo^4", "relator^4", "sumario", "txt_integral", "txt_parcial", "descritores^3"]


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
