from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from datetime import datetime, timedelta
from jurisapp.models import Acordao
from jurisapp import pdf


def index(request):
    return render(request, 'jurisapp/index.html')


    # individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    # descritores are in a concatenated string, split them into list
    ac.set_descritores_to_list()

    context_dict = {'acordao': ac}
    return render(request, 'jurisapp/acordao.html', context_dict)


def acordao_pdf(request, acordao_id):
    ac = Acordao.objects.get(pk=acordao_id)
    # todo make this a method and call from above too
    ac.set_descritores_to_list()

    absolute_uri = request.build_absolute_uri()
    pdf_doc = pdf.get_acordao_pdf(ac, absolute_uri)

    response = HttpResponse(pdf_doc, content_type='application/pdf')
    filename = ac.tribunal_id + " - " + ac.processo + ".pdf"
    response['Content-Disposition'] = 'filename="' + filename + '"'
    return response


def recent_acordaos(request):
    most_recent_date = Acordao.objects.aggregate(Max('date_loaded'))['date_loaded__max']
    recent_date = most_recent_date - timedelta(days=3)
   # recent_date = datetime.now() - timedelta(days=3)
    acordaos = Acordao.objects.filter(date_loaded__gte=recent_date).order_by('-data')
    for acordao in acordaos:
        acordao.set_descritores_to_list()
    context_dict = {'acordaos': acordaos}
    return render(request, 'jurisapp/recent_acordaos.html', context_dict)