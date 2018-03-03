from django.shortcuts import render
from .models import Acordao
from . import search as s


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

    page = request.GET.get('page')
    if page is None:
        page = 1

    display = 10
    try:
        page = int(page)
    except ValueError:
        page = 1

    results = s.and_search(query, tribs, page, display, sort_by)

    total = results['total']
    acordaos = results['acordaos']

    total_pages = get_total_pages(total, display)

    context_dict = dict(total=total, acordaos=acordaos, query=query, tribs=tribs, page=page,
                        has_next=results['has_next'], has_previous=results['has_previous'], total_pages=total_pages)
    return render(request, 'jurisapp/search_results.html', context_dict)


def get_total_pages(total, display):
    total_pages = total // display
    if total % display is not 0:
        total_pages = total_pages + 1
    return total_pages


# individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)
