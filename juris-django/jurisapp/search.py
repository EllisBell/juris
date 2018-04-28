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

    # Remember to specify analyzer to stem words correctly etc.
    # By default, queries will use the analyzer defined in the index mapping for the field
    mappings = {"acordao": {
        "properties": {
            "id": {"type": "integer"},
            # Todo test these keywords out -send in capitalized, uncapitalized etc.
            "processo": {"type": "text"},
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

    index_client.create(index="acordao_idx", body={"mappings": mappings})


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


# def search_fields(index, query, searchable_fields, match_type, operator, sort_by, filter_dict, exclude_from_res,
#                   start_at=0, res_size=10):
#     #es = get_es()
#     body = get_multi_match_query(query, searchable_fields, match_type, operator)
#     body = add_sort(body, sort_by)
#     if filter_dict:
#         body = add_filter(body, filter_dict)
#     #res = es.search(index=index, body=body, _source_exclude=exclude_from_res, from_=start_at, size=res_size)
#     res = do_search(index, body, exclude_from_res, start_at, res_size)
#     return res

def search_fields(sd):
    #es = get_es()
    body = get_multi_match_query(sd.query, sd.searchable_fields, sd.match_type, sd.operator)
    body = add_sort(body, sd.sort_by)
    if sd.filter_dict:
        body = add_filter(body, sd.filter_dict)
    #res = es.search(index=index, body=body, _source_exclude=exclude_from_res, from_=start_at, size=res_size)
    res = do_search(sd.index, body, sd.exclude, sd.start_at, sd.res_size)
    return res

#def search_with_date_range()


def do_search(index, body, exclude, start_at, res_size):
    es = get_es()
    res = es.search(index=index, body=body, _source_exclude=exclude, from_=start_at, size=res_size)
    return res


def get_basic_multi_match_query(query, fields, match_type, operator):
    query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "type": match_type,
                "operator": operator
            }
        }
    }
    return query


def get_multi_match_query(query, fields, match_type, operator):
    query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": fields,
                        "type": match_type,
                        # n.b. we still need to include "and" here if we want ALL the terms in query
                        # to be present
                        "operator": operator
                    }
                }
            }
        }
    }

    return query


def add_sort(query_dict, sort_field):
    if not sort_field:
        sort_field = "_score"
    query_dict["sort"] = [{sort_field: "desc"}]
    return query_dict


def add_filter(query_dict, filter_dict):
    query_dict["query"]["bool"]["filter"] = get_filter(filter_dict)
    return query_dict


def get_filter(filter_dict):
    filters = []
    for key, value in filter_dict.items():
        filters.append({"terms": {key: value}})
    return filters


def add_date_range(query_dict, date_from, date_to):
    query_dict["query"]["bool"]["must"]["range"]["data"] = {"gte": date_from, "lte": date_to}
    return query_dict


def search_field(query, field):
    return None
