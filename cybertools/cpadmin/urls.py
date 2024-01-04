from django.urls import path
from . import views, views_weapons, views_armor, views_gear

urlpatterns = [
    # Route to home
    path('', views.index, name='index'),

    # Routes to characters
    path('characters/', views.characters_home, name='characters'),

    # Routes to equipment
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

    path('equipment/cyberware', views_armor.list, name='cyberware'),

    path('equipment/clothes', views_armor.list, name='clothes'),

    # Routes to drugs
    path('drugs/', views.drugs_home, name='drugs'),

    # Routes to vehicles
    path('vehicles/', views.vehicles_home, name='vehicles'),

    # Routes to netrunning
    path('netrunning/', views.netrunning_home, name='netrunning'),

    # Routes to complements
    path('complements/', views.complements_home, name='complements'),
]
