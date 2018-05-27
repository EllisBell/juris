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

    # OK
    # Essentially, wanted:
    # a) To avoid a query for e.g. artigo 127 matching cases with processo number e.g. 127/abc-p2
    # This was happening because the ES analyzer (portuguese) was splitting on "/" (amongst others)
    # b) To still allow for searching cross_fields including processo number
    # e.g. 127/abc-p2 materia de facto
    # cross_fields only works if the fields being searched in are indexed with the same analyzer,
    # so have left processo being analyzed with portuguese analyzer like other full text fields
    # But that was causing problem a)
    # To avoid problem a), now also indexing processo and text fields (sumario, txt_integral etc.) in such a way
    # that only the words in those fields that contain numbers are indexed, and are left untouched
    # E.g. 127/abc-p2 would remain 127/abc-p2 in that version of the field
    # This pattern matches words that don't contain any numbers (we want to exclude these in our custom analyzer)
    no_num_pattern = "^[^0-9]+$"

    settings = {"analysis": {
        "analyzer": {
          "words_with_numbers": {
              "type": "custom",
              "tokenizer": "whitespace",
              "filter": ["lowercase", "non_nums_remover", "remove_empty"]
          }
        },
        "filter": {
          "non_nums_remover": {
              "type": "pattern_replace",
              "pattern": no_num_pattern,
              "replacement": ""
          },
          "remove_empty": {
              "type": "stop",
              "stopwords": [""]
            }
        },
        "normalizer": {
            "lowercase_ascii": {
                "type": "custom",
                "filter": ["lowercase", "asciifolding"]
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
                             "raw": {"type": "keyword", "normalizer": "lowercase_ascii"},
                             "just_with_nums": {"type": "text", "analyzer": "words_with_numbers"}
                         }
                         },
            "tribunal": {"type": "keyword"},
            "tribunal_long": {"type": "keyword"},
            # TODO see if this works ok, might be better off having it as keyword, or with custom analyzer
            # todo e.g. just to remove accents or something
            "relator": {"type": "text", "analyzer": "portuguese"},
            "sumario": {"type": "text", "analyzer": "portuguese",
                        "fields": {
                            "just_with_nums": {"type": "text", "analyzer": "words_with_numbers"}
                        }
                        },
            "txt_integral": {"type": "text", "analyzer": "portuguese",
                             "fields": {
                                 "just_with_nums": {"type": "text", "analyzer": "words_with_numbers"}
                             }
                             },
            "txt_parcial": {"type": "text", "analyzer": "portuguese",
                            "fields": {
                                "just_with_nums": {"type": "text", "analyzer": "words_with_numbers"}
                            }
                            },
            "descritores": {"type": "text", "analyzer": "portuguese",
                            "fields": {
                                "just_with_nums": {"type": "text", "analyzer": "words_with_numbers"}
                            }
                            },
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
    # TODO probably best to check that trib property exists
    # todo otherwise will break when getting id_name/long_name
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


# analyzes text
def test_normalise(normaliser, text):
    es = get_es()
    index_client = es.indices
    return index_client.analyze(body={"normalizer": normaliser, "text": text})


# what we're going for when creating the query is something like this:
# e.g. query is 'orange grape "red onion" OR apple banana'
# {query :
#   {bool:
#     {must:
#       {bool:[
#         {should: - at least one of these bools has to match
#           {bool:     (for each component of or)
#             {must: [{multi_match query (many fields / phrase)} orange & grape
#                    {multi_match query (many fields / phrase)} "red onion" (phrase)]
#           {bool:
#             {must: [{multi_match query (many fields / phrase)} apple & banana]
#           ]
#     {filter: {filter dict}
#     {sort: {sort dict}
#
# todo to deal with processo, plan is to try adding a should to each of the above or component bools
# todo matching just on processo with an or
def search_fields(sd):
    body = get_query_outline()
    outer_bool_dict = {'bool': {}}
    body["query"] = outer_bool_dict

    if sd.query_components:
        middle_bool_dict = {'bool': {}}
        middle_bool_dict = get_should_bool_dict(middle_bool_dict, sd)
        # then add that to outer bool dict
        add_to_bool(outer_bool_dict, "must", middle_bool_dict)

    # Adding filters to outer bool
    if sd.from_date:
        body = add_date_range_filter(body, sd.from_date, sd.to_date)
    if sd.filter_dict:
        body = add_terms_filter_new(body, sd.filter_dict)

    body = add_sort(body, sd.sort_by)
    print("BODY")
    print(body)

    res = do_search(sd.index, body, sd.exclude, sd.start_at, sd.res_size)
    return res


def get_should_bool_dict(bool_dict, sd):
    query_components = sd.query_components
    # There might be no query
    if not query_components:
        return bool_dict

    # query components is a list of lists of dicts
    # each component was a part of the original query separated by or
    # the dicts in each component are either normal cross_fields query
    # or a phrase query
    # or a cross_fields query for just words with nums (using different versions of searchable fields)
    for query_comp in query_components:
        # query_comp is a list of dicts
        inner_bool_dict = {'bool': {}}
        for query_dict in query_comp:
            # where there are numbers involved
            if query_dict["is_words_with_nums"]:
                multi_match_dict = get_multi_match_query(query_dict["query"], sd.searchable_fields_with_nums,
                                                         query_dict["type"], "and")
                add_to_bool(inner_bool_dict, "must", multi_match_dict)
            else:
                multi_match_dict = get_multi_match_query(query_dict["query"], sd.searchable_fields,
                                                     query_dict["type"], "and")
                add_to_bool(inner_bool_dict, "must", multi_match_dict)

        # add to the bool dict should clause
        add_to_bool(bool_dict, "should", inner_bool_dict)

    return bool_dict


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
            "operator": operator,
        }
    }

    return multi_match_dict


def get_match_query(query, field, operator):
    match_dict = {
        "match": {
            field: {
                "query": query,
                "operator": operator
            }
        }
    }

    return match_dict


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
