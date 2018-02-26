import json
from elasticsearch import Elasticsearch, helpers
from .models import Acordao


def get_es():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    return es


# analyzes text
def test_analyse(analyser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"analyzer": analyser, "text": text})


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


def index_acordao(ac_doc, ac_id):
    es = get_es()
    es.index(index="acordao_idx", doc_type="acordao", body=ac_doc, id=ac_id)


def count_indexed_acordaos(es):
    return es.count(index="acordao_idx", doc_type="acordao")


# Todo need something that will index on update of acordao table

def search_all_fields(query, match_type, operator, return_source=True):
    es = get_es()
    fields = get_searchable_fields()
    body = get_multi_match_query(query, fields, match_type, operator)
    res = es.search(index="acordao_idx", body=body, _source=return_source)
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


def search_field(query, field):
    return None


def search():
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
