from django.urls import path
from . import views

urlpatterns = [
    # Route to home
    path('', views.index, name='index'),

    # Routes to characters
    path('characters/', views.equipment_home, name='characters'),

    # Routes to equipment
    path('equipment/', views.equipment_home, name='equipment'),
    path('equipment/weapons', views.weapons_list, name='weapons'),
    path('equipment/weapons/create', views.weapons_create),
    path('equipment/weapons/update', views.weapons_update),
    path('equipment/weapons/delete', views.weapons_delete),
    path('equipment/weapons/download', views.weapons_download),
    path('equipment/weapons/upload', views.weapons_upload),
    path('equipment/weapons/refresh', views.weapons_refresh),

    # Routes to drugs
    path('drugs/', views.equipment_home, name='drugs'),

    # Routes to vehicles
    path('vehicles/', views.equipment_home, name='vehicles'),

    # Routes to netrunning
    path('netrunning/', views.equipment_home, name='netrunning'),

    # Routes to complements
    path('complements/', views.equipment_home, name='complements'),
]
