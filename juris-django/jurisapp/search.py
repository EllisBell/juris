import json
from elasticsearch import Elasticsearch, helpers
from .models import Acordao
from datetime import datetime


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


def bulk_index_acordaos(timeout):
    print("changed", str(timeout))
    es = get_es()
    actions = get_bulk_actions()
    helpers.bulk(es, actions, request_timeout=timeout)


# Use generator
def get_bulk_actions():
    acordaos = Acordao.objects.all()
    for ac in acordaos.iterator():
        doc = create_acordao_doc_with_desc(ac)
        yield {"_index": "acordao_idx",
               "_type": "acordao",
               "_id": ac.acordao_id,
               "_source": doc
               }


# TODO figure out how to update index rather than deleting and reindexing everything
# todo as that takes quite a while

# TODO try denormalizing acordao descritores to improve indexing performance? avoid loads of db calls

# Todo add other properties, including descritores...
# todo add descritores as array
def create_acordao_doc(ac):
    doc = {"processo": ac.processo,
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
    descritores = [desc.descritor for desc in ac.acordaodescritor_set.all()]
    doc["descritores"] = descritores
    return doc


# interface
def index_acordao(ac):
    doc = create_acordao_doc_with_desc(ac)
    index_acordao_with_id(doc, ac.acordao_id)


def index_acordao_with_id(ac_doc, ac_id):
    es = get_es()
    es.index(index="acordao_idx", doc_type="acordao", body=ac_doc, id=ac_id)


# interface
def count_indexed_acordaos(es):
    return es.count(index="acordao_idx", doc_type="acordao")


# Todo need something that will index on update of acordao table


## Search Interface ##

# TODO what to do with this
default_query_type = "most_fields"


# analyzes text
def test_analyse(analyser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"analyzer": analyser, "text": text})


# interface
# Main search, called from view
def and_search(query, tribs, page_number, display_size, sort_by=None):
    return search_with_paging(query, tribs, "and", page_number, display_size, sort_by)


def or_search(query, tribs, page_number, display_size, sort_by=None):
    return search_with_paging(query, tribs, "or", page_number, display_size, sort_by)


def phrase_search(query, tribs, page_number, display_size, sort_by=None):
    return search_with_paging(query, tribs, "and", page_number, display_size, sort_by, "phrase")


def search(query, tribs, operator):
    res = search_all_fields(query, default_query_type, operator, tribs)
    return get_ids_from_res(res)


def search_with_paging(query, tribs, operator, page_number, display_size, sort_by, query_type="most_fields"):
    if not page_number:
        page_number = 1

    print("in search with paging, query is " + query)
    start = (page_number - 1) * display_size
    res = search_all_fields(query, query_type, operator, sort_by, tribs, start, display_size)
    results = get_results_dict_from_res(res)
    total = results['total']
    print("in search with paging, total is " + str(total))
    has_next = (page_number * display_size) < total
    has_previous = (page_number is not 1) and (page_number - 1) * display_size < total
    results['has_next'] = has_next
    results['has_previous'] = has_previous
    return results


def get_ids_from_res(res):
    res_data = res['hits']['hits']
    ac_ids = [hit["_id"] for hit in res_data]
    return ac_ids


def get_results_dict_from_res(res):
    results = {}
    results['total'] = res['hits']['total']
    results['acordaos'] = [d['_source'] for d in res['hits']['hits']]

    for acordao, hit in zip(results['acordaos'], res['hits']['hits']):
        acordao['id'] = hit['_id']

    for acordao in results['acordaos']:
        acordao['data'] = datetime.strptime(acordao['data'], "%Y-%m-%d")

    return results


def search_all_fields(query, match_type, operator, sort_by, tribs=None, start_at=0, res_size=10):
    es = get_es()
    fields = get_searchable_fields()
    body = get_multi_match_query(query, fields, match_type, operator)
    body = add_sort(body, sort_by)
    if tribs:
        body = add_filter(body, "tribunal", tribs)
    print("body is")
    print(body)
    res = es.search(index="acordao_idx", body=body, _source_exclude=['tribunal', 'txt_integral', 'txt_parcial'],
                    from_=start_at, size=res_size)
    return res


def get_searchable_fields():
    return ["processo^2", "relator^2", "sumario", "txt_integral", "txt_parcial", "descritores^2"]


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


def add_filter(query_dict, field, values):
    query_dict["query"]["bool"]["filter"] = get_filter(field, values)
    return query_dict


def get_filter(field, values):
    return {"terms": {field: values}}


# todo complete
def convert_es_res_to_acordaos(res):
    res_data = res['hits']['hits']  # list of dicts
    # Convert results to list of acordao objects with fields to display in search results
    for ac_dict in res_data:
        source = ac_dict['source']
        ac = Acordao()
        ac.processo = ac_dict["processo"]
        ac.relator = ac_dict["relator"]
        ac.tribunal = ac_dict["tribunal"]
        ac.sumario = ac_dict["sumario"]
        ac.txt_integral = ac_dict["txt_integral"]
        ac.txt_parcial = ac_dict["txt_parcial"]
        ac.data = ac_dict["data"]


def search_field(query, field):
    return None


def asearch():
    return None
    # Definitely want to use multi match, question is what type
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
    # e.g. es.search(index="acordao_idx", body=
    # {"query":{"multi_match":
    # {"query":"privilegio creditos banana trabalhadores",
    # "fields":["descritores", "txt_parcial"],
    # "operator":"and"
    # }}},
    # _source=False)
