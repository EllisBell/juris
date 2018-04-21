from django.shortcuts import render
from django.http import HttpResponse
from .models import Acordao, SearchHistory
from . import acordao_search
from raven.contrib.django.raven_compat.models import client



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

    page = get_page(request)
    display = 10

    try:
        results = acordao_search.get_search_results(query, tribs, page, display, sort_by)

    except Exception:
        # Log error to Sentry
        client.captureException()
        # TODO return error page
        return render(request, 'jurisapp/oops.html')

    total = results['total']
    acordaos = results['acordaos']
    total_pages = get_total_pages(total, display)

    context_dict = dict(total=total, acordaos=acordaos, query=query, tribs=tribs, page=page,
                        has_next=results['has_next'], has_previous=results['has_previous'], total_pages=total_pages)
    return render(request, 'jurisapp/search_results.html', context_dict)


def save_search(request):
    query = request.GET['query']
    acordao_search.save_search(query)
    # status 204 is no content
    return HttpResponse(status=204)


def get_page(request):
    page = request.GET.get('page')
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
    return page


def get_total_pages(total, display):
    total_pages = total // display
    if total % display is not 0:
        total_pages = total_pages + 1
    return total_pages


# individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    # descritores are in a concatenated string, split them into list
    descritores = ac.descritores
    desc_list = descritores.split("|")
    ac.descritores = desc_list
    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)
