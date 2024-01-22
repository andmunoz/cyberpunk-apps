from django.shortcuts import render
from cpadmin.views.views_weapons import list as weapons_list
from cpadmin.views.views_drugs import list as drugs_list
from cpadmin.views.views_vehicles import list as vehicles_list


### Function for Home
def index(request):
    return render(request, 'index.html')


### Functions for Characters Section
def characters_home(request):
    return render(request, 'error_404.html', context={'image':'characters.jpg'})


### Functions for Equipment Section
def equipment_home(request):
    return weapons_list(request)


### Functions for Drugs Section
def drugs_home(request):
    return drugs_list(request)


### Functions for Vehicles Section
def vehicles_home(request, type='land'):
    return vehicles_list(request, type)

### Functions for Netrunning Section
def netrunning_home(request):
    return render(request, 'error_404.html', context={'image':'netrunning.jpg'})


### Functions for Complements Section
def complements_home(request):
    return render(request, 'error_404.html', context={'image':'complements.jpg'})


### Functions for Custom 404
def custom_404(request):
    return render(request, 'error_404.html', context={'image':'complements.jpg'})
