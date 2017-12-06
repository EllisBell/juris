from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Acordao
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import F
from . import acordao_search


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
    term = query
    print("got query")
    page = request.GET.get('page')
    print("page is:")
    print(page)
    if page is None:
        page = 1

    print("NOW PAGE IS")
    print(page)

    num_per_page = 25
   # current_offset = (page - 1) * num_per_page

    # TODO ok this isn't going to work as it returns just the limit amount
    # todo so paginator will only have that amount and only have 1 page
    # todo may want to set paginator.count to the total by running a count query and returning it as well?
    #acordao_results = acordao_search.search_acordaos(query, num_per_page, current_offset)

    # Evaluate results so can count to paginator as list
    # Otherwise it can't use raw query set
    #acordao_results = [acordao for acordao in acordao_results]

    # UPDATE Added searchvectorfield to Acordao model; this seems to work pretty well
    #acordao_results = Acordao.objects.filter(searchable_idx_col=SearchQuery(query, config='tuga'))

    ## LOOK AT THIS - using ranking - have to use F to get value of searchable_idx_col
    search_query = SearchQuery(query, config='tuga')
    acordao_results = Acordao.objects.annotate(rank=SearchRank(F('searchable_idx_col'), search_query))\
        .filter(searchable_idx_col=search_query).order_by('-rank')

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
    context_dict = {'total': paginator.count, 'acordaos': acordaos, 'query': term}
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
