from django.shortcuts import render
from cpadmin.views.views_weapons import list as weapons_list
from cpadmin.views.views_drugs import list as drugs_list


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
    return drugs_list(request)


### Functions for Vehicles Section
def vehicles_home(request):
    return render(request, 'index.html')


### Functions for Netrunning Section
def netrunning_home(request):
    return render(request, 'index.html')


### Functions for Complements Section
def complements_home(request):
    return render(request, 'index.html')
