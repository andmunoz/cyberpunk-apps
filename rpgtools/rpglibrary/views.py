import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

# Create your views here.
def index(request, actual_folder=""):
    base_folder = os.path.join(settings.BASE_DIR, "documents", actual_folder)
    if not os.path.exists(base_folder) or not os.path.isdir(base_folder):
        raise Http404("Folder not found")
    elements = []
    for item in os.listdir(base_folder):
        item_route = os.path.join(base_folder, item)
        relative_route = os.path.join(actual_folder, item).replace(os.sep, "/")
        if os.path.isdir(item_route):
            elements.append({
                "tipo": "folder",
                "nombre": item,
                "ruta": f"/{relative_route}/"
            })
        else:
            elements.append({
                "tipo": "file",
                "nombre": item,
                "ruta": f"{settings.MEDIA_URL}{relative_route}"
            })
    parent = os.path.dirname(actual_folder).replace(os.sep, "/")
    if parent != "":
        parent_folder = f"/{parent}/"
    else:
        parent_folder = "/"
    actual_folder_list = []
    for afolder in actual_folder.split('/'):
        if len(actual_folder_list) > 0:
            actual_folder_list.append({
                "name": afolder, 
                "url": str(actual_folder_list[len(actual_folder_list)-1]) + "/" + afolder,
            })
        else: 
            actual_folder_list.append({
                "name": afolder, 
                "url": afolder,
            })
    content = {
        "elements": elements,
        "actual_folder": actual_folder,
        "actual_folder_list": actual_folder_list,
        "parent_folder": parent_folder,
    }
    return render(request, 'index.html', content)