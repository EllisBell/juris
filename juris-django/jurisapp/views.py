from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Acordao
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import F
from . import acordao_search


def index(request):
    return render(request, 'jurisapp/index.html')


def search(request):
    query = request.GET['query']
    print("got query")

    # n.b. the [] after tribs is apparently inserted by jQuery (even though we are passing 'tribs' it adds the '[]')
    tribs = request.GET.getlist('tribs[]')
    if tribs:
        print("got tribs...")
        print(tribs)

    page = request.GET.get('page')
    print("page is:")
    print(page)
    if page is None:
        page = 1

    print("NOW PAGE IS")
    print(page)

    ## LOOK AT THIS - using ranking - have to use F to get value of searchable_idx_col
    search_query = SearchQuery(query, config='tuga')
    ## NB filtering on acordao as well
    acordao_results = Acordao.objects.annotate(rank=SearchRank(F('searchable_idx_col'), search_query)) \
        .filter(searchable_idx_col=search_query, tribunal__in=tribs).order_by('-rank')

    # AND / OR / PHRASE search
    # The above query translates into a plainto_tsquery function call in sql. This joins terms with an & by default
    # So need to account for OR searches or full phrase search

    paginator = Paginator(acordao_results, 25)

    try:
        # request may or may not have come with a page number
        acordaos = paginator.page(page)
    except PageNotAnInteger:
        # if no page number, deliver the first page
        acordaos = paginator.page(1)
    except EmptyPage:
        # if page out of range, deliver last page of results
        acordaos = paginator.page(paginator.num_pages)

    print("got total")
    # TODO the query we pass has to be the search term
    context_dict = {'total': paginator.count, 'acordaos': acordaos, 'query': query, 'tribs': tribs}
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


def get_acordaos(query, tribs):
    if '*' in query:
        results = or_search(query, tribs)
    else:
        results = and_search(query, tribs)

    return results


def and_search(query, tribs):
    return get_results(SearchQuery(query), tribs)


def or_search(query, tribs):
    words = query.split('*')
    search_query = SearchQuery()
    for word in words:
        search_query = search_query & SearchQuery(word)

    return get_results(search_query, tribs)


def get_results(search_query, tribs):
    return Acordao.objects.annotate(rank=SearchRank(F('searchable_idx_col'), search_query)) \
        .filter(searchable_idx_col=search_query, tribunal__in=tribs).order_by('-rank')


# individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)
