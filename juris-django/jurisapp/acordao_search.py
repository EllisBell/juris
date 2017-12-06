from .models import Acordao


def search_acordaos(query, limit, offset):
    # TODO nb. using raw sql is much much faster for some reason
    # todo by the way the above raw sql breaks when passing more than one word to query term
    # todo yet to try indexing vectored column and using that (with and without raw sql)
    # todo also look at paging - i think displaying all results is delaying things

    # filter(search=SearchQuery(query, config='tuga'))

    # query_string = """select acordao_id from acordao where to_tsvector('tuga', coalesce(txt_integral,''))
    #    @@ to_tsquery('tuga', %s)"""

    # get query with right operators
    query = get_qualified_query(query)

    # Searching across multiple columns with ranking; cols weighted differently. Concatenated ts_vector in where clause
    # is indexed
    # TODO consider passing in different weights array to ts_rank_cd
    # TODO watch for string.format if you do this as postgres array uses {} braces
    query_string = """select acordao_id, ts_rank_cd(searchable_idx_col, query) rank
        from acordao, to_tsquery('tuga', %s) as query where searchable_idx_col @@ query
        order by rank desc limit {0} offset {1}""".format(limit, offset)

    res = Acordao.objects.raw(query_string, [query])
    return res


def get_qualified_query(query):
    if (query[0] == "\"" and query[-1] == "\"") or (query[0] == "'" and query[-1] == "'"):
        query.replace("\"", "")
        query.replace("'", "")
        words = query.split()
        query = "<->".join(words)
    # revamp but this is the general idea
    elif 'OR' in query:
        query = query.replace('OR', '')
        words = query.split()
        query = "|".join(words)
    # if not in quotes or or, it is an and search
    else:
        words = query.split()
        query = "&".join(words)
    return query
