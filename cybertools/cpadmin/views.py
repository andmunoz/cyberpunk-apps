from django.shortcuts import render
from .views_equipment import weapons_list


### Function for Home
def index(request):
    return render(request, 'index.html')


### Functions for Characters Section
def characters_home(request):
    return render(request, 'index.html')


### Functions for Equipment Section
def equipment_home(request):
    return weapons_list(request)


### Functions for Drugs Section
def drugs_home(request):
    return render(request, 'index.html')


### Functions for Vehicles Section
def vehicles_home(request):
    return render(request, 'index.html')


### Functions for Netrunning Section
def netrunning_home(request):
    return render(request, 'index.html')


### Functions for Complements Section
def complements_home(request):
    return render(request, 'index.html')
