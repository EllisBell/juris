from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Acordao
from . import acordao_search
from raven.contrib.django.raven_compat.models import client
from . import pdf
import json


def index(request):
    return render(request, 'jurisapp/index.html')


def search_relevant(request):
    return search(request)


def search_recent(request):
    return search(request, "data")


# TODO clean this up
# TODO allow for and search, or search, phrase search
# TODO and sorting by date / relevance
def search(request, sort_by=None):
    query = request.GET['query']

    # n.b. the [] after tribs is apparently inserted by jQuery (even though we are passing 'tribs' it adds the '[]')
    tribs = request.GET.getlist('tribs[]')

    processo = request.GET['processo']
    print("PROC " + processo)
    from_date = request.GET['fromDate']
    print(from_date)
    to_date = request.GET['toDate']

    page = get_page(request)
    display = 10

    asd = acordao_search.AcordaoSearchData(query=query, tribs=tribs, processo=processo,
                                           from_date=from_date, to_date=to_date, page_number=page)

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


# individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    # descritores are in a concatenated string, split them into list
    convert_descritores_to_list(ac)

    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)


def acordao_pdf(request, acordao_id):
    ac = Acordao.objects.get(pk=acordao_id)
    # todo make this a method and call from above too
    convert_descritores_to_list(ac)

    absolute_uri = request.build_absolute_uri()
    pdf_doc = pdf.get_acordao_pdf(ac, absolute_uri)

    response = HttpResponse(pdf_doc, content_type='application/pdf')
    filename = ac.tribunal_id + " - " + ac.processo + ".pdf"
    response['Content-Disposition'] = 'filename="' + filename + '"'
    return response


def convert_descritores_to_list(ac):
    descritores = ac.descritores
    desc_list = descritores.split("|")
    ac.descritores = desc_list


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