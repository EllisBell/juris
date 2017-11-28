from django.shortcuts import render
from django.http import HttpResponse
from .models import Acordao
from django.contrib.postgres.search import SearchQuery, SearchVector


# Create your views here.
# placeholder just to get started
def index(request):
    return render(request, 'jurisapp/index.html')


# experiment with postgres full text search
# gonna need a template with a search box
# and some javascript
# n.b. current thinking is just do this in vanilla js
# no jquery, no frameworks
# improve js while doing it
# and then learn a framework and make another proj with it
def search(request):
    query = request.GET['query']

    #acordaos = Acordao.objects.annotate(search=SearchVector('txt_integral', config='tuga')).filter(search=SearchQuery(query, config='tuga'))

    query_string = """select acordao_id from acordao where to_tsvector('tuga', coalesce(txt_integral,'')) 
    @@ to_tsquery('tuga', %s)"""

    # split query into multiple words
    query = get_qualified_query(query)

    # Searching across multiple columns with ranking; cols weighted differently. Concatenated ts_vector in where clause
    # is indexed
    query_string = """select acordao_id, ts_rank_cd('{0.01, 0.2, 0.4, 1.0}', searchable_idx_col, query) rank
    from acordao, to_tsquery('tuga', %s) as query where searchable_idx_col @@ query
    order by rank desc"""
    res = Acordao.objects.raw(query_string, [query])
    # TODO nb. using raw sql is much much faster for some reason
    # todo by the way the above raw sql breaks when passing more than one word to query term
    # todo yet to try indexing vectored column and using that (with and without raw sql)
    # todo also look at paging - i think displaying all results is delaying things
    print("got to here")
    # total = Acordao.objects.filter(txt_integral__contains=query).count()
    acordao_list = list(res)
    total = len(acordao_list)
    print("got total")
    acordaos = acordao_list
    context_dict = {'total': total, 'acordaos': acordaos}
    print("and to here")
    return render(request, 'jurisapp/search_results.html', context_dict)

    # postgres full text search
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/search/
    # https://www.postgresql.org/docs/current/static/textsearch.html
    # e.g. search on txt_integral Acordao.objects.filter(txt_integral__search='crimes')

    # current plan:
    # get a lot of data to really test out search performance (and check what kind of size)
    # try implementing search on all relevant columns (e.g. search for a term and it searches across all cols)
    # in PSQL:
    # do it normally, check performance
    # do it with postgres full text search (using ts_query, ts_vector etc.)
    # if necessary try indexing - see what works best: indexing each search column vs one index concatenating all
    # then try replicating through Django
    # n.b. (still need to fix todo below) - index on txt_integral worked like a charm
    # question is whether to concatenate all columns to index, so that can search across all
    # or have individual indices (may be necessary for weighting)
    # TODO note: postgres giving error when using ts_vector: word too long to be indexed (larger than 2047 chars)
    # todo find out where these are / why they exist - see board for more info


    # useful to know when in PSQL "explain analyze <query>" to get cost and explain plan

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
