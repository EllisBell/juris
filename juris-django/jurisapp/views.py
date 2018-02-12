from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Acordao
from . import acordao_search


def index(request):
    return render(request, 'jurisapp/index.html')


def search(request):
    query = request.GET['query']

    # n.b. the [] after tribs is apparently inserted by jQuery (even though we are passing 'tribs' it adds the '[]')
    tribs = request.GET.getlist('tribs[]')

    page = request.GET.get('page')
    if page is None:
        page = 1

    acordao_results = acordao_search.get_acordaos(query, tribs)
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

    context_dict = {'total': paginator.count, 'acordaos': acordaos, 'query': query, 'tribs': tribs}
    return render(request, 'jurisapp/search_results.html', context_dict)

    # postgres full text search
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/search/
    # https://www.postgresql.org/docs/current/static/textsearch.html


# individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)
