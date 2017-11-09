from django.shortcuts import render
from django.http import HttpResponse
from .models import Acordao


# Create your views here.
# placeholder just to get started
def index(request):
    acordaos = Acordao.objects.all()
    acordao_string = ""
    for acordao in acordaos:
        acordao_string += "<br>d" + str(acordao)
    return HttpResponse(acordao_string)

# experiment with postgres full text search
# gonna need a template with a search box
# and some javascript
# n.b. current thinking is just do this in vanilla js
# no jquery, no frameworks
# improve js while doing it
# and then learn a framework and make another proj with it
def search(request):
    return None
    # postgres full text search
    #https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/search/
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


    # useful to know when in PSQL "explain <query>" to get cost