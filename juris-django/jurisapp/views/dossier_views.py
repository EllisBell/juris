from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from jurisapp.models import Folder

def dossier_home(request):
    # TODO poor man's feature toggle, remove when ready
    if not settings.DEBUG:
        return redirect('juris_index')
    if not request.user.is_authenticated:
        return render(request, 'jurisapp/dossier/dossier_landing.html')

    current_user = request.user
    folders = current_user.folder_set.all()

    context_dict = {'folders': folders}
    
    return render(request, 'jurisapp/dossier/dossier.html', context_dict)

@login_required
def folder_detail(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)

    context_dict = {'folder': folder}

    return render(request, 'jurisapp/dossier/folder_detail.html', context_dict)



