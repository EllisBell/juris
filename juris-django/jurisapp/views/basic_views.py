from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.utils import timezone
from jurisapp.models import Acordao, Folder, Tribunal
from jurisapp import pdf
from jurisapp.forms import SaveAcordaoForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'jurisapp/index.html')


# individual acordao
def acordao(request, acordao_id):
    ac = Acordao.objects.get(pk=acordao_id)
    # descritores are in a concatenated string, split them into list
    ac.set_descritores_to_list()

    ac_folders = []
    all_folders = []
    if request.user.is_authenticated:
        folders = get_acordao_folders(ac, request.user)
    else:
        folders = ([], [])
    
    form = SaveAcordaoForm({'acordao_id': acordao_id})

    context_dict = {'acordao': ac, 'form': form, 'ac_folders': folders[0], 'all_folders': folders[1]}
    return render(request, 'jurisapp/acordao.html', context_dict)

def get_acordao_folders(acordao, user):
    ac_folders = acordao.folder_set.filter(archived=False)
    all_folders = user.folder_set.filter(archived=False)
    user_ac_folders = [ac_folder for ac_folder in ac_folders if ac_folder in all_folders]
    available_folders_for_saving = [folder for folder in all_folders if folder not in user_ac_folders]
    return (user_ac_folders, available_folders_for_saving)


def get_folder_list_snippet(request):
    acordao_id = request.GET.get("acordao_id", None)
    if acordao_id:
        ac = Acordao.objects.get(pk=acordao_id)
        folders = get_acordao_folders(ac, request.user)

        context_dict = {'ac_folders': folders[0]}
        return render(request, 'jurisapp/snippets/folder_list_snippet.html', context_dict)


def acordao_pdf(request, acordao_id):
    ac = Acordao.objects.get(pk=acordao_id)
    ac.set_descritores_to_list()

    absolute_uri = request.build_absolute_uri()
    pdf_doc = pdf.get_acordao_pdf(ac, absolute_uri)

    response = HttpResponse(pdf_doc, content_type='application/pdf')
    filename = ac.tribunal_id + " - " + ac.processo + ".pdf"
    response['Content-Disposition'] = 'filename="' + filename + '"'
    return response

all_tribs_in_order = ["STJ", "TRL", "TRP", "TRC", "TRG", "TRE"]


def recent_acordaos(request):
    tribs = request.GET.getlist('trib', None)
    acordaos = Acordao.objects.recent_by_trib(tribs).select_related('tribunal')

    for acordao in acordaos:
        acordao.set_descritores_to_list()

    all_tribs = Tribunal.objects.all()
    all_tribs = sorted(all_tribs, key=lambda x: all_tribs_in_order.index(x.id_name) if x.id_name in all_tribs_in_order else 100)
    
    all_active_tribs = tribs or [trib.id_name for trib in all_tribs]
    active_tribs = {trib: True for trib in all_active_tribs} 

    for trib in all_tribs:
        others = ["trib={}".format(other) for other in active_tribs if other != trib.id_name]
        link = "&".join(others)
        if not active_tribs.get(trib.id_name, False):
            link += "&trib={}".format(trib.id_name)
        trib.link = link

    context_dict = {'acordaos': acordaos, "active_tribs": active_tribs, "all_tribs": all_tribs}
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