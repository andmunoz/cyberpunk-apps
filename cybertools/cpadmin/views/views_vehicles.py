from django.shortcuts import render, redirect, HttpResponse
import csv, json
from cpadmin.models import (
    ItemType, Category, Brand, Vehicle
)
from cpadmin.config import get_database, get_type, get_translated_object, download_csv


# Show vehicle list
def list(request, type='land'):
    vehicles = Vehicle.objects.filter(type=get_type(Vehicle.Type, value=type)).order_by('name')
    vehicle_count = 0
    if vehicles:
        vehicle_count = len(vehicles)

    parents = Category.objects.filter(type='VEHICLE', code=get_type(Vehicle.Type, value=type)).order_by('name')
    categories = Category.objects.filter(type='VEHICLE', parent=parents.first().id).order_by('name')
    brands = Brand.objects.filter(type='VEHICLE').order_by('name')
    title = Vehicle.Type(get_type(Vehicle.Type, value=type)).label

    context = {
        'page_title': title,
        'vehicle_count': vehicle_count,
        'vehicles': vehicles,
        'categories': categories,
        'brands': brands,
        'vehicle_type': type,
    }
        
    return render(request, 'vehicles/vehicle.html', context)


# Create an vehicle
def create(request, type='land'):
    form = request.POST
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    vehicle = Vehicle(
        name=form['name'],
        category=category,
        brand=brand,
        type=form['type'],
        top_speed=int(form['top_speed']),
        acceleration=int(form['acceleration']),
        deceleration=int(form['deceleration']),
        crew=int(form['crew']),
        passengers=int(form['passengers']),
        autonomy=int(form['autonomy']),
        cargo=int(form['cargo']),
        maneuverability=int(form['maneuverability']),
        sp=int(form['sp']),
        sdp=int(form['sdp']),
        weight=float(form['weight']),
        cost=int(form['cost']),
        description=form['description'],
        image=form['image'],
    )
    vehicle.save()

    return redirect('/vehicles/' + type)


# Update an vehicle
def update(request, type='land'):
    form = request.POST
    vehicle = Vehicle.objects.get(id=form['id'])
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    vehicle.name = form['name']
    vehicle.category = category
    vehicle.brand = brand
    vehicle.type = get_type(Vehicle.Type, form['type'])
    vehicle.top_speed = int(form['top_speed'])
    vehicle.acceleration = int(form['acceleration'])
    vehicle.deceleration = int(form['deceleration'])
    vehicle.crew = int(form['crew'])
    vehicle.passengers = int(form['passengers'])
    vehicle.autonomy = int(form['autonomy'])
    vehicle.cargo = int(form['cargo'])
    vehicle.maneuverability = int(form['maneuverability'])
    vehicle.sp = int(form['sp'])
    vehicle.sdp = int(form['sdp'])
    vehicle.weight = float(form['weight'])
    vehicle.cost = int(form['cost'])
    vehicle.description = form['description']
    vehicle.image = form['image']
    vehicle.save()
    
    return redirect('/vehicles/' + type)


# Delete an vehicle
def delete(request, type='land'):
    form = request.POST
    vehicle = Vehicle.objects.get(id=form['id'])
    vehicle.delete()
    return redirect('/vehicles/' + type)


# Upload vehicle list from CSV
def upload(request, type='land'):
    csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        category = Category.objects.get(name=row['category'], type=ItemType.VEHICLE)
        brand, _ = Brand.objects.get_or_create(
            name=row['brand'], type=ItemType.VEHICLE,
            defaults={'name': row['brand'], 'type': ItemType.VEHICLE, 'description': 'Autogenerated'})

        Vehicle.objects.update_or_create(
            id=row['id'],
            defaults=dict(
                name=row['name'],
                category=category,
                brand=brand,
                type=row['type'],
                top_speed=int(row['top_speed']),
                acceleration=int(row['acceleration']),
                deceleration=int(row['deceleration']),
                crew=int(row['crew']),
                passengers=int(row['passengers']),
                autonomy=int(row['autonomy']),
                cargo=int(row['cargo']),
                maneuverability=int(row['maneuverability']),
                sp=int(row['sp']),
                sdp=int(row['sdp']),
                weight=float(row['weight']),
                cost=int(row['cost']),
                description=row['description'],
                image=row['image'],
            )
        )
        
    return redirect('/vehicles/' + type)


# Download vehicle list in CSV
def download(request, type='land'):
    vehicles = Vehicle.objects.filter(type=get_type(Vehicle.Type, value=type)).order_by('name')
    return download_csv(Vehicle, vehicles)


# Refresh vehicle list with Firebase
def refresh(request, type='land'):
    database = get_database()
    if database is None:
        return redirect('/vehicles/' + type)
    source = request.POST['source']
    if source == 'local': 
        vehicles_local = Vehicle.objects.all().order_by('id').values()
        database.child('Catalog/Vehicles').remove()
        for vehicle in vehicles_local:
            translated_vehicle = vehicle # get_translated_object(Vehicle, vehicle)
            database.child('Catalog/Vehicles').push(translated_vehicle)
    else:
        vehicle_origin = database.child('Catalog/Vehicles').get()
        for vehicle_id, vehicle in vehicle_origin:
            category = Category.objects.get(code=vehicle.category)
            brand, _ = Brand.objects.get_or_create(
                name=vehicle.brand, 
                defaults={'name': vehicle.brand, 'type': ItemType.VEHICLE, 'description': 'Autogenerated'})
            
            Vehicle.objects.update_or_create(
                id=vehicle_id,
                defaults=dict(
                    name=vehicle.name,
                    category=category,
                    brand=brand,
                    type=vehicle.type,
                    top_speed=vehicle.top_speed,
                    acceleration=vehicle.acceleration,
                    deceleration=vehicle.deceleration,
                    crew=vehicle.crew,
                    passengers=vehicle.passengers,
                    autonomy=vehicle.autonomy,
                    cargo=vehicle.cargo,
                    maneuverability=vehicle.maneuverability,
                    sp=vehicle.sp,
                    sdp=vehicle.sdp,
                    weight=vehicle.weight,
                    cost=vehicle.cost,
                    description=vehicle.description,
                    image=vehicle.image,
                ),
            )

    return redirect('/vehicles/' + type)
