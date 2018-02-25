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
def create_acordao_index():
    es = get_es()
    index_client = es.indices

    mappings = {"acordao": {
        "properties": {
            "processo": {"type": "keyword"},
            "sumario": {"type": "text", "analyzer": "portuguese"},
            "data": {"type": "date"}
        }
    }
    }

    index_client.create(index="acordao_idx", body={"mappings": mappings})


def bulk_index_acordaos():
    es = get_es()
    actions = get_bulk_actions()
    helpers.bulk(es, actions)


# Use generator
def get_bulk_actions():
    for ac in Acordao.objects.all()[:10]:
        doc = create_acordao_doc(ac)
        yield {"_index": "acordao_idx",
               "_type": "acordao",
               "_source": doc
               }


def create_acordao_doc(ac):
    doc = {"processo": ac.processo, "sumario": ac.sumario, "data": ac.data}
    return doc


def count_indexed_acordaos(es):
    return es.count(index="acordao_idx", doc_type="acordao")

# Need something that will index on update of acordao table
