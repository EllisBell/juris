from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from raven.contrib.django.raven_compat.models import client
import json
from jurisapp.models import Acordao
from jurisapp import acordao_search



def search_relevant(request):
    return search(request)

# data is date
def search_recent(request):
    return search(request, "data")


# TODO clean this up
# TODO allow for and search, or search, phrase search
# TODO and sorting by date / relevance
def search(request, sort_by=None):
    query = request.GET['query']

    # n.b. the [] after tribs is apparently inserted by jQuery (even though we are passing 'tribs' it adds the '[]')
    tribs = request.GET.getlist('tribs[]')
    acordao_ids = request.GET.getlist('acordao_ids[]')

    processo = request.GET['processo']
    print("PROC " + processo)
    from_date = request.GET['fromDate']
    print(from_date)
    to_date = request.GET['toDate']

    just_txt_integral = request.GET['justTxtIntegral'] == 'true'

    page = get_page(request)
    display = 10

    asd = acordao_search.AcordaoSearchData(query=query, tribs=tribs, processo=processo, acordao_ids=acordao_ids,
                                           from_date=from_date, to_date=to_date, page_number=page, 
                                           just_txt_integral=just_txt_integral)

    try:
        # results = acordao_search.get_search_results(query, tribs, page, display, sort_by)
        results = acordao_search.get_search_results(asd, display, sort_by)

    except Exception as e:
        if settings.DEBUG:
            raise e
        else:
            # Log error to Sentry
            client.captureException()
        # TODO return error page
        return render(request, 'jurisapp/oops.html')

    total = results['total']

    if total == 0:
        return render(request, 'jurisapp/no_results.html')


    acordaos = results['acordaos']
    total_pages = get_total_pages(total, display)

    context_dict = dict(total=total, acordaos=acordaos, query=query, tribs=tribs, page=page,
                        has_next=results['has_next'], has_previous=results['has_previous'], total_pages=total_pages,
                        processo=processo, from_date=from_date, to_date=to_date)
    return render(request, 'jurisapp/search_results.html', context_dict)


# query can be for dossier names, comments
# or for acordaos themselves (through ES)
# start by doing just the ES
# so to here, pass the query string, and a list of acordao IDs to filter by
# (the acordao IDs of all your saved acordaos, or just the ones in the dossier you are in)
def dossier_search(request):
    query = request.GET['query']




def get_page(request):
    page = request.GET.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
    return page


def get_total_pages(total, display):
    total_pages = total // display
    if total % display is not 0 or total == 0:
        total_pages = total_pages + 1
    return total_pages


def save_search(request):
    if not settings.DEBUG:
        query = request.GET['query']
        acordao_search.save_search(query)
        # status 204 is no content
    return HttpResponse(status=204)


def suggest_processo(request):
    proc = request.GET.get('term', '')

    print(proc)
    suggestions = get_suggestions(proc)
    # jquery autocomplete specific
    results = []
    for proc in suggestions:
        print(proc)
        proc_json = {'value': proc, 'label': proc}
        results.append(proc_json)
    data = json.dumps(results)

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def get_suggestions(proc):
    suggs = Acordao.objects.filter(processo__istartswith=proc).only("processo")
    just_procs = [sugg.processo for sugg in suggs]
    return just_procs
    #return []
