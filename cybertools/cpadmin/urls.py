from django.urls import path
from cpadmin.views import (
    views, 
    views_weapons, views_armor, views_gear, views_cyberware, views_clothes,
    views_drugs, views_medical,
    views_vehicles
)

urlpatterns = [
    # Route to home
    path('', views.index, name='home'),

    # Routes to characters section
    path('characters/', views.characters_home, name='characters'),

    # Routes to equipment section
    path('equipment/', views.equipment_home, name='equipment'),
    
    path('equipment/weapons', views_weapons.list, name='weapons'),
    path('equipment/weapons/create', views_weapons.create),
    path('equipment/weapons/update', views_weapons.update),
    path('equipment/weapons/delete', views_weapons.delete),
    path('equipment/weapons/download', views_weapons.download),
    path('equipment/weapons/upload', views_weapons.upload),
    path('equipment/weapons/refresh', views_weapons.refresh),

    path('equipment/armor', views_armor.list, name='armor'),
    path('equipment/armor/create', views_armor.create),
    path('equipment/armor/update', views_armor.update),
    path('equipment/armor/delete', views_armor.delete),
    path('equipment/armor/download', views_armor.download),
    path('equipment/armor/upload', views_armor.upload),
    path('equipment/armor/refresh', views_armor.refresh),

    path('equipment/gear', views_gear.list, name='gear'),
    path('equipment/gear/create', views_gear.create),
    path('equipment/gear/update', views_gear.update),
    path('equipment/gear/delete', views_gear.delete),
    path('equipment/gear/download', views_gear.download),
    path('equipment/gear/upload', views_gear.upload),
    path('equipment/gear/refresh', views_gear.refresh),

    path('equipment/cyberware', views_cyberware.list, name='cyberware'),
    path('equipment/cyberware/create', views_cyberware.create),
    path('equipment/cyberware/update', views_cyberware.update),
    path('equipment/cyberware/delete', views_cyberware.delete),
    path('equipment/cyberware/download', views_cyberware.download),
    path('equipment/cyberware/upload', views_cyberware.upload),
    path('equipment/cyberware/refresh', views_cyberware.refresh),

    path('equipment/clothes', views_clothes.list, name='clothes'),
    path('equipment/clothes/create', views_clothes.create),
    path('equipment/clothes/update', views_clothes.update),
    path('equipment/clothes/delete', views_clothes.delete),
    path('equipment/clothes/download', views_clothes.download),
    path('equipment/clothes/upload', views_clothes.upload),
    path('equipment/clothes/refresh', views_clothes.refresh),

    # Routes to medical and drugs section
    path('drugs/', views.drugs_home, name='drugs_and_medical'),

    path('drugs/drug', views_drugs.list, name='drugs'),
    path('drugs/drug/create', views_drugs.create),
    path('drugs/drug/update', views_drugs.update),
    path('drugs/drug/delete', views_drugs.delete),
    path('drugs/drug/download', views_drugs.download),
    path('drugs/drug/upload', views_drugs.upload),
    path('drugs/drug/refresh', views_drugs.refresh),

    path('drugs/medical', views_medical.list, name='medical'),
    path('drugs/medical/create', views_medical.create),
    path('drugs/medical/update', views_medical.update),
    path('drugs/medical/delete', views_medical.delete),
    path('drugs/medical/download', views_medical.download),
    path('drugs/medical/upload', views_medical.upload),
    path('drugs/medical/refresh', views_medical.refresh),

    # Routes to vehicles section
    path('vehicles/', views.vehicles_home, name='vehicles'),
    
    path('vehicles/spacecrafts', views.custom_404, name='spacecrafts'),

    path('vehicles/acpa', views.custom_404, name='powered_armors'),

    path('vehicles/remotes', views.custom_404, name='remotes'),

    path('vehicles/options', views.custom_404, name='vehicle_options'),

    path('vehicles/<str:type>', views.vehicles_home, name='category_vehicles'),
    path('vehicles/<str:type>/create', views_vehicles.create),
    path('vehicles/<str:type>/update', views_vehicles.update),
    path('vehicles/<str:type>/delete', views_vehicles.delete),
    path('vehicles/<str:type>/download', views_vehicles.download),
    path('vehicles/<str:type>/upload', views_vehicles.upload),
    path('vehicles/<str:type>/refresh', views_vehicles.refresh),
    
    # Routes to netrunning section
    path('netrunning/', views.netrunning_home, name='netrunning'),

    # Routes to complements section
    path('complements/', views.complements_home, name='complements'),
]
