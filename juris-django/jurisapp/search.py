from elasticsearch import Elasticsearch, helpers
from .models import Acordao
import datetime
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
            "processo": {"type": "keyword"},
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
    print("started at " + str(datetime.datetime.now()))
    es = get_es()
    actions = get_bulk_actions(just_new)
    helpers.bulk(es, actions, request_timeout=timeout)
    print("finished at " + str(datetime.datetime.now()))


def parallel_bulk(just_new, timeout):
    print("started at " + str(datetime.datetime.now()))
    es = get_es()
    actions = get_bulk_actions(just_new)
    deque(helpers.parallel_bulk(es, actions, request_timeout=timeout), maxlen=0)
    print("finished at " + str(datetime.datetime.now()))


# Use generator
def get_bulk_actions(just_new):
    if just_new:
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

# TODO try denormalizing acordao descritores to improve indexing performance? avoid loads of db calls

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
def index_acordao(ac):
    doc = create_acordao_doc_with_desc(ac)
    index_doc(doc)


def index_doc(doc):
    es = get_es()
    es.index(index="acordao_idx", doc_type="acordao", body=doc)


# interface
def count_indexed_acordaos(es):
    return es.count(index="acordao_idx", doc_type="acordao")


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

def db_test():
    start = datetime.datetime.now()

    acordaos = Acordao.objects.all()
    for ac in acordaos:
        print(ac.processo)

    print("start at " + str(start))
    print("end at " + str(datetime.datetime.now))


# Search Interface #

# TODO what to do with this
default_query_type = "most_fields"


# analyzes text
def test_analyse(analyser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"analyzer": analyser, "text": text})


def search_fields(index, query, searchable_fields, match_type, operator, sort_by, filter_dict, exclude_from_res,
                  start_at=0, res_size=10):
    es = get_es()
    body = get_multi_match_query(query, searchable_fields, match_type, operator)
    body = add_sort(body, sort_by)
    if filter_dict:
        body = add_filter(body, filter_dict)
    res = es.search(index=index, body=body, _source_exclude=exclude_from_res, from_=start_at, size=res_size)
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


def search_field(query, field):
    return None
