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
            "processo": {"type": "keyword"},
            "sumario": {"type": "text", "analyzer": "portuguese"},
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


def create_acordao_doc(ac):
    doc = {"processo": ac.processo, "sumario": ac.sumario, "data": ac.data}
    return doc


def count_indexed_acordaos(es):
    return es.count(index="acordao_idx", doc_type="acordao")

# Need something that will index on update of acordao table
