from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import F
from .models import Acordao


def get_acordaos(query, tribs):
    if query[0] == "\"" and query[-1] == "\"":
        results = phrase_search(query, tribs)
    elif ' ou ' in query.lower():
        results = or_search(query, tribs)
    else:
        results = and_search(query, tribs)

    return results


def and_search(query, tribs):
    return get_query_filtering_on_search_query(get_search_query(query), tribs)


def or_search(query, tribs):
    words = [word.strip() for word in query.lower().split('ou')]
    search_query = get_search_query(words[0])
    for word in words:
        # combine SearchQuery objects with OR operator for or search
        search_query = search_query | get_search_query(word)

    return get_query_filtering_on_search_query(search_query, tribs)


def phrase_search(query, tribs):
    search_query = get_search_query(query)
    query = query.replace("\"", "")
    words = query.split()
    query = "<->".join(words)

    query_set = get_basic_query(search_query, tribs)
    query_set = query_set.extra(where=["searchable_idx_col @@ to_tsquery(%s, %s)"], params=['tuga', query])
    return query_set


def get_search_query(query):
    return SearchQuery(query, config='tuga')


def get_query_filtering_on_search_query(search_query, tribs):
    # Filtering on SearchQuery translates into a plainto_tsquery function call in sql.
    # This joins terms with an & by default
    return get_basic_query(search_query, tribs).filter(searchable_idx_col=search_query)


def get_basic_query(search_query, tribs):
    return Acordao.objects.annotate(rank=SearchRank(F('searchable_idx_col'), search_query)) \
        .filter(tribunal__in=tribs).order_by('-rank')
