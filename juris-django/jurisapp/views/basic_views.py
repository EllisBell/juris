from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from datetime import datetime, timedelta
from django.utils import timezone
from jurisapp.models import Acordao, Folder
from jurisapp import pdf
from jurisapp.forms import SaveAcordaoForm


def index(request):
    return render(request, 'jurisapp/index.html')


    # individual acordao
def acordao(request, acordao_id):
    print("got to acordao view")
    ac = Acordao.objects.get(pk=acordao_id)
    # descritores are in a concatenated string, split them into list
    ac.set_descritores_to_list()

    ac_folders = []
    all_folders = []
    if request.user.is_authenticated:
        ac_folders = ac.folder_set.all()
        all_folders = request.user.folder_set.all()
    
    form = SaveAcordaoForm({'acordao_id': acordao_id})

    context_dict = {'acordao': ac, 'form': form, 'ac_folders': ac_folders, 'all_folders': all_folders}
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


# TODO check if user is authenticated
# TODO on acordao page show button if user not logged in,
# but show pop up explaining can't do it (or redirect to dossier landing page)
# TODO don't submit form without an acordao name being input or an existing being selected
def save_acordao(request):    
    if request.method == 'POST':
        form = SaveAcordaoForm(request.POST)

        if form.is_valid():
            acordao_id = form.cleaned_data.get('acordao_id')
            folder_id = form.cleaned_data.get('dossier_id')
            folder_name = form.cleaned_data.get('dossier_name')
            folder_desc = form.cleaned_data.get('dossier_description')
            current_user = request.user
            current_time = timezone.now()

            if folder_id is None:
                folder = Folder(
                    name=folder_name, 
                    description=folder_desc,
                    created_at = current_time,
                    created_by = current_user
                )
                folder.save()
            else:
                folder = get_object_or_404(Folder, pk=folder_id)
            
            acordao = get_object_or_404(Acordao, pk=acordao_id)
            current_user = request.user

            folder.acordaos.add(acordao, through_defaults={'saved_at':current_time, 'saved_by': current_user})
            folder.users.add(current_user)

            return JsonResponse({'folder_name': folder.name})