from elasticsearch import Elasticsearch, helpers
from .models import Acordao
from collections import deque


def get_es():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    return es


# indexing a doc using es.index would normally create index if didn't exist
# but we want to specify analyzer for index so think I need to specifically create one with mappings etc.
def create_acordao_idx():
    es = get_es()
    index_client = es.indices

    settings = {"analysis": {
        "normalizer": {
            "lowercaser": {
                "type": "custom",
                "filter": "lowercase"
            }
        }
    }}

    # Remember to specify analyzer to stem words correctly etc.
    # By default, queries will use the analyzer defined in the index mapping for the field
    mappings = {"acordao": {
        "properties": {
            "id": {"type": "integer"},
            # Todo test these keywords out -send in capitalized, uncapitalized etc.
            "processo": {"type": "text", "analyzer": "portuguese",
                         "fields": {
                             "raw": {"type": "keyword", "normalizer": "lowercaser"}
                         }
                         },
            "tribunal": {"type": "keyword"},
            "tribunal_long": {"type": "keyword"},
            # TODO see if this works ok, might be better off having it as keyword, or with custom analyzer
            # todo e.g. just to remove accents or something
            "relator": {"type": "text", "analyzer": "portuguese"},
            "sumario": {"type": "text", "analyzer": "portuguese"},
            "txt_integral": {"type": "text", "analyzer": "portuguese"},
            "txt_parcial": {"type": "text", "analyzer": "portuguese"},
            "descritores": {"type": "text", "analyzer": "portuguese"},
            "data": {"type": "date"}
        }
    }
    }

    index_client.create(index="acordao_idx", body={"settings": settings, "mappings": mappings})


def delete_acordao_idx():
    es = get_es()
    index_client = es.indices

    index_client.delete("acordao_idx")


def bulk_index_acordaos(just_new, timeout):
    es = get_es()
    actions = get_bulk_actions(just_new)
    helpers.bulk(es, actions, request_timeout=timeout)


def parallel_bulk(just_new, timeout):
    es = get_es()
    actions = get_bulk_actions(just_new)
    deque(helpers.parallel_bulk(es, actions, request_timeout=timeout), maxlen=0)


# Use generator
def get_bulk_actions(just_new):
    if just_new and count_indexed_acordaos() > 0:
        max_id_already_indexed = get_max_id()
        acordaos = Acordao.objects.filter(acordao_id__gt=max_id_already_indexed)
    else:
        acordaos = Acordao.objects.all()
    for ac in acordaos.iterator():
        doc = create_acordao_doc_with_desc(ac)
        yield {"_index": "acordao_idx",
               "_type": "acordao",
               "_source": doc
               }


# TODO figure out how to update index rather than deleting and reindexing everything
# todo as that takes quite a while

def create_acordao_doc(ac):
    doc = {"id": ac.acordao_id,
           "processo": ac.processo,
           "tribunal": ac.tribunal.id_name,
           "tribunal_long": ac.tribunal.long_name,
           "relator": ac.relator,
           "sumario": ac.sumario,
           "txt_integral": ac.txt_integral,
           "txt_parcial": ac.txt_parcial,
           "data": ac.data
           }
    return doc


def create_acordao_doc_with_desc(ac):
    doc = create_acordao_doc(ac)
    descritores = ac.descritores
    desc_list = []
    # Descritores are stored in DB as concatenated string to avoid having to make several trips to DB as that
    # was very slow. Break them up into string here to send list into es
    if descritores:
        desc_list = descritores.split("|")
    doc["descritores"] = desc_list
    return doc


# interface

class SearchData:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


def index_acordao(ac):
    doc = create_acordao_doc_with_desc(ac)
    index_doc(doc)


def index_doc(doc):
    es = get_es()
    es.index(index="acordao_idx", doc_type="acordao", body=doc)


# interface
def count_indexed_acordaos():
    es = get_es()
    return es.count(index="acordao_idx", doc_type="acordao")['count']


def get_max_id():
    body = {"query": {
        "match_all": {}
    },
        "sort": {
            "id": "desc"
        }
    }
    es = get_es()
    res = es.search(index="acordao_idx", body=body, _source_include=["id"], size=1)
    return res['hits']['hits'][0]['_source']['id']


# Todo need something that will index on update of acordao table


# Search Interface #

# TODO what to do with this
default_query_type = "most_fields"


# analyzes text
def test_analyse(analyser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"analyzer": analyser, "text": text})


def search_fields(sd):
    print("GOT TO SEARCH FIELDS")

    body = get_query_outline()
    outer_bool_dict = {'bool': {}}
    body["query"] = outer_bool_dict
    if sd.query:
        multi_match_dict = get_multi_match_query(sd.query, sd.searchable_fields, sd.match_type, sd.operator)
        bool_dict = body["query"]
        add_to_bool(bool_dict, "must", multi_match_dict)
        # bool_dict = append_multi_match(outer_bool_dict, sd.query, sd.searchable_fields, sd.match_type, sd.operator, "must")
        # body["query"] = bool_dict
    if sd.from_date:
        body = add_date_range_filter(body, sd.from_date, sd.to_date)
    if sd.filter_dict:
        body = add_terms_filter_new(body, sd.filter_dict)
    if sd.phrases:
        bool_dict = body["query"]
        for phrase in sd.phrases:
            bool_dict = append_multi_match(bool_dict, phrase, sd.searchable_fields, "phrase", sd.operator, "must")
        body["query"] = bool_dict

    body = add_sort(body, sd.sort_by)
    print("BODY")
    print(body)

    res = do_search(sd.index, body, sd.exclude, sd.start_at, sd.res_size)
    return res


def do_search(index, body, exclude, start_at, res_size):
    es = get_es()
    res = es.search(index=index, body=body, _source_exclude=exclude, from_=start_at, size=res_size)
    return res


def get_query_outline():
    query = {
        "query": {

        }
    }

    return query


# Add multi_match to query dict MUST
# pass it a bool value (must or should)
# if value already in dict, add to its list
# If it doesn't, add to bool dict, and add this to list
def append_multi_match(dict_with_bool, query, fields, match_type, operator, bool_val):
    multi_match_dict = {"multi_match": {
        "query": query,
        "fields": fields,
        "type": match_type,
        # n.b. we still need to include "and" here if we want ALL the terms in query
        # to be present
        "operator": operator
    }
    }

    # check if bool_val is in bool dict
    # todo extract this into method
    # if bool_val in query_dict["query"]["bool"]:
    #     query_dict["query"]["bool"][bool_val].append(multi_match_dict)
    # else:
    #     query_dict["query"]["bool"][bool_val] = [multi_match_dict, ]

    # TODO pass in the target dict to this method
    add_to_bool(dict_with_bool, bool_val, multi_match_dict)

    return dict_with_bool


# date range is always must (when there)
# check if "must" in bool dict, if not, add it
def add_date_range_filter(query_dict, date_from, date_to):
    print("ADDING DATE RANGE, " + date_from)
    # if no end date provided, range is from_date to from_date
    if not date_to:
        date_to = date_from

    date_dict = {"range": {"data": {"gte": date_from, "lte": date_to, "format": "dd/MM/yyyy"}}}
    # Add as filter to outer bool
    add_to_bool(query_dict["query"], "filter", date_dict)
    print("HERE")

    return query_dict


def add_sort(query_dict, sort_field):
    if not sort_field:
        sort_field = "_score"
    query_dict["sort"] = [{sort_field: "desc"}]
    return query_dict


# def add_terms_filter(query_dict, filter_dict):
#     terms_filter_list = get_terms_filter_list(filter_dict)
#     if "filter" in query_dict["query"]["bool"]:
#         query_dict["query"]["bool"]["filter"].extend(terms_filter_list)
#     else:
#         query_dict["query"]["bool"]["filter"] = get_terms_filter_list(filter_dict)
#
#     return query_dict


def add_terms_filter_new(query_dict, filter_dict):
    terms_filter_list = get_terms_filter_list(filter_dict)
    bool_dict = query_dict["query"]
    for filter_d in terms_filter_list:
        add_to_bool(bool_dict, "filter", filter_d)

    return query_dict


# filter_dict is like e.g. {"tribs":["trl", "trp", "trc"], "processo": ["abc/123.p1", ]}
def get_terms_filter_list(filter_dict):
    filters = []
    for key, value in filter_dict.items():
        filters.append({"terms": {key: value}})
    return filters


def get_multi_match_query(query, fields, match_type, operator):
    multi_match_dict = {
            "multi_match": {
                "query": query,
                "fields": fields,
                "type": match_type,
                "operator": operator
            }
        }

    return multi_match_dict


def add_to_bool(dict_with_bool, bool_type, dict_to_add):
    # takes a dict with bool key
    # bool type should be must, should, filter or something
    # checks if must, should, filter already exists, if does, add to list
    # if not, add and add list
    if bool_type in dict_with_bool["bool"]:
        dict_with_bool["bool"][bool_type].append(dict_to_add)
    else:
        dict_with_bool["bool"][bool_type] = [dict_to_add, ]




def search_field(query, field):
    return None
