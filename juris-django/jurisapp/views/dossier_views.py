from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from jurisapp.models import Folder
from jurisapp.forms import CreateFolderForm
from jurisapp import acordao_search
from django.utils import timezone

def dossier_home(request):
    # TODO poor man's feature toggle, remove when ready
    # if not settings.DEBUG:
    #     return redirect('juris_index')
    if not request.user.is_authenticated:
        return render(request, 'jurisapp/dossier/dossier_landing.html')

    current_user = request.user
    folders = current_user.folder_set.all().filter(archived=False).order_by('-created_at')

    context_dict = {'folders': folders, 'user_name': current_user.first_name}
    
    return render(request, 'jurisapp/dossier/dossier.html', context_dict)

@login_required
def dossier_archive(request):
    folders = request.user.folder_set.all().filter(archived=True).order_by('-created_at')

    context_dict = {'folders': folders}
    
    return render(request, 'jurisapp/dossier/dossier_archive.html', context_dict)

# TODO check folder belongs to user
@login_required
def folder_detail(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)

    context_dict = {'folder': folder}

    return render(request, 'jurisapp/dossier/folder_detail.html', context_dict)

@login_required
def dossier_search(request):
    query = request.GET['query']
    dossier_id = request.GET.get('dossier_id', None)
    archived = request.GET.get('archived', False)

    current_user = request.user
    user_folders = current_user.folder_set.all().filter(archived=archived)

    folder_acordao_ids = []

    for folder in user_folders:
        acs = folder.acordaos.all()
        ac_ids = [ac.acordao_id for ac in acs]
        together = (folder.id, ac_ids)
        folder_acordao_ids.append(together)

    all_acordao_ids = [ac_id for fa in folder_acordao_ids for ac_id in fa[1]]

    asd = acordao_search.AcordaoSearchData(query=query, acordao_ids=all_acordao_ids, tribs=None, processo=None, 
                                            from_date=None, to_date=None, page_number=1)

    results = acordao_search.get_search_results(asd, 1000, sort_by=None)

    acordaos = results['acordaos']

    folder_acordaos = []

    for folder in user_folders:
        match = [tup for tup in folder_acordao_ids if tup[0] == folder.id][0]
        ac_ids = match[1]
        this_folder_acordaos = [acordao for acordao in acordaos if acordao["id"] in ac_ids]
        together = (folder, this_folder_acordaos)
        folder_acordaos.append(together)

    folder_acordaos = [folder_acordao for folder_acordao in folder_acordaos if folder_acordao[1]]

    matching_folders = [folder for folder in user_folders if query.lower() in folder.name.lower() or query.lower() in folder.description.lower()]

    context_dict = {'query': query, 'folder_acordaos': folder_acordaos, 'folders': matching_folders}

    return render(request, 'jurisapp/dossier/dossier_search_results.html', context_dict)

# TODO check folder belongs to user
@login_required
def edit_folder(request):
    new_name = request.POST.get('folder_name', None)
    new_description = request.POST.get('folder_description', None)
    folder_id = request.POST.get('folder_id', None)
    if folder_id:
        folder_id_num = int(folder_id)
        folder = Folder.objects.get(pk=folder_id_num)
        folder.name = new_name if new_name else folder.name
        folder.description = new_description if new_description else folder.description
        folder.save()
    return HttpResponse(status=204)

@login_required
def new_folder(request):
    if request.method == 'POST':
        form = CreateFolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.created_at = timezone.now()
            folder.created_by = request.user

            folder.save()
            folder.users.add(request.user)
            return redirect('dossier_home')
    else:
        form = CreateFolderForm()

    return render(request, 'jurisapp/dossier/new_folder.html', {'form': form})

# TODO check folder belongs to user
@login_required
def archive_folder(request):
    return set_folder_archived(request, True)

# TODO check folder belongs to user
@login_required
def unarchive_folder(request):
    return set_folder_archived(request, False)

def set_folder_archived(request, archived):
    folder_id = request.POST.get('folder_id', None)
    if folder_id:
        folder = Folder.objects.get(pk=folder_id)
        folder.archived = archived
        folder.save()
        return HttpResponse(status=204)
    
    return HttpResponse(status=404)



