from django.urls import path
from . import views, views_equipment

urlpatterns = [
    # Route to home
    path('', views.index, name='index'),

    # Routes to characters
    path('characters/', views.characters_home, name='characters'),

    # Routes to equipment
    path('equipment/', views.equipment_home, name='equipment'),
    
    path('equipment/weapons', views_equipment.weapons_list, name='weapons'),
    path('equipment/weapons/create', views_equipment.weapons_create),
    path('equipment/weapons/update', views_equipment.weapons_update),
    path('equipment/weapons/delete', views_equipment.weapons_delete),
    path('equipment/weapons/download', views_equipment.weapons_download),
    path('equipment/weapons/upload', views_equipment.weapons_upload),
    path('equipment/weapons/refresh', views_equipment.weapons_refresh),

    path('equipment/armor', views_equipment.armor_list, name='armor'),
    path('equipment/armor/create', views_equipment.armor_create),
    path('equipment/armor/update', views_equipment.armor_update),
    path('equipment/armor/delete', views_equipment.armor_delete),
    path('equipment/armor/download', views_equipment.armor_download),
    path('equipment/armor/upload', views_equipment.armor_upload),
    path('equipment/armor/refresh', views_equipment.armor_refresh),

    # Routes to drugs
    path('drugs/', views.drugs_home, name='drugs'),

    # Routes to vehicles
    path('vehicles/', views.vehicles_home, name='vehicles'),

    # Routes to netrunning
    path('netrunning/', views.netrunning_home, name='netrunning'),

    # Routes to complements
    path('complements/', views.complements_home, name='complements'),
]
