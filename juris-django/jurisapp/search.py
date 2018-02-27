import json
from elasticsearch import Elasticsearch, helpers
from .models import Acordao


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
        doc = create_acordao_doc(ac)
        yield {"_index": "acordao_idx",
               "_type": "acordao",
               "_id": ac.acordao_id,
               "_source": doc
               }


# Todo add other properties, including descritores...
# todo add descritores as array
def create_acordao_doc(ac):
    doc = {"processo": ac.processo,
           "tribunal": ac.tribunal.id_name,
           "relator": ac.relator,
           "sumario": ac.sumario,
           "txt_integral": ac.txt_integral,
           "txt_parcial": ac.txt_parcial,
           "data": ac.data
           }
    return doc


def create_acordao_doc_with_desc(ac):
    doc = create_acordao_doc(ac)
    descritores = []
    for desc in ac.acordaodescritor_set.all():
        descritores.append(desc.descritor)
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

# analyzes text
def test_analyse(analyser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"analyzer": analyser, "text": text})


# interface
# Main search, called from view
def search(query):
    # get just ids
    res = search_all_fields(query, "best_fields", "and", False)
    return get_ids_from_res(res)


def search_with_paging(query, page_number, display_size):
    if not page_number:
        page_number = 1

    start = (page_number - 1) * display_size
    res = search_all_fields(query, "best_fields", "and", False, start, display_size)
    return get_ids_from_res(res)


def get_ids_from_res(res):
    res_data = res['hits']['hits']
    ac_ids = [hit["_id"] for hit in res_data]
    return ac_ids


def search_all_fields(query, match_type, operator, return_source=True, start_at=0, res_size=10):
    es = get_es()
    fields = get_searchable_fields()
    body = get_multi_match_query(query, fields, match_type, operator)
    res = es.search(index="acordao_idx", body=body, _source=return_source, from_=start_at, size=res_size)
    return res


def get_searchable_fields():
    return ["processo", "relator", "sumario", "txt_integral", "txt_parcial", "descritores"]


def get_multi_match_query(query, fields, match_type, operator):
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


def get_multi_match_query_with_tribs(query, tribs, fields, match_type, operator):
    query = {
        "query": {
            "bool": {
                operator: {
                    "multi_match": {
                        "query": query,
                        "fields": fields,
                        "type": match_type
                    }
                },
                "filter": {
                    "terms": {
                        "tribunal": tribs
                    }
                }
            }
        }
    }

    return query


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
