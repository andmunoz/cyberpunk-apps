from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, Brand, Vehicle, VehicleType
)
from cpadmin.config import get_database


# Get id of a Type Choice
def get_type(value):
    return VehicleType[value.upper()].value


# Get humanized dictionary from Object
def get_translated_object(vehicle):
    return {
        'id': vehicle.id,
        'name': vehicle.name,
        'brand': vehicle.brand.name,
        'type': vehicle.get_type_display(),
        'category': vehicle.category.name,
        'top_speed': str(vehicle.top_speed) + ' km/h',
        'acceleration': str(vehicle.acceleration) + ' m/s',
        'deceleration': str(vehicle.deceleration) + ' m/s',
        'range': str(vehicle.range) + ' kms',
        'crew': vehicle.crew,
        'passengers': vehicle.passengers,
        'cargo': str(vehicle.cargo) + ' kgs',
        'maneuverability': ('+' if vehicle.maneuverability > 0 else '') + str(vehicle.maneuverability),
        'sp': vehicle.sp,
        'sdp': vehicle.sdp,
        'weight': str(vehicle.weight) + ' kgs',
        'cost': str(vehicle.cost) + ' creds',
        'description': vehicle.description,
        'image': vehicle.image,
    }


# Show vehicle list
def list(request, type):
    vehicles = Vehicle.objects.filter(type=get_type(type)).order_by('name')
    vehicle_count = 0
    if vehicles:
        vehicle_count = len(vehicles)

    parents = Category.objects.filter(type='VEHICLE', code=get_type(type)).order_by('name')
    categories = Category.objects.filter(type='VEHICLE', parent=parents.first().id).order_by('name')
    brands = Brand.objects.filter(type='VEHICLE').order_by('name')
    title = VehicleType(get_type(type)).label

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
def create(request, type):
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
        range=int(form['range']),
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
def update(request, type):
    form = request.POST
    vehicle = Vehicle.objects.get(id=form['id'])
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    vehicle.name = form['name']
    vehicle.category = category
    vehicle.brand = brand
    vehicle.type = get_type(form['type'])
    vehicle.top_speed = int(form['top_speed'])
    vehicle.acceleration = int(form['acceleration'])
    vehicle.deceleration = int(form['deceleration'])
    vehicle.crew = int(form['crew'])
    vehicle.passengers = int(form['passengers'])
    vehicle.range = int(form['range'])
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
def delete(request, type):
    form = request.POST
    vehicle = Vehicle.objects.get(id=form['id'])
    vehicle.delete()
    return redirect('/vehicles/' + type)


# Upload vehicle list from CSV
def upload(request, type):
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
                range=int(row['range']),
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
def download(request, type):
    vehicles = Vehicle.objects.filter(type=get_type(type)).order_by('name')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vehicles.csv"'
    csv_writer = csv.writer(response)

    vehicles_translated = []
    for vehicle in vehicles:
        vehicles_translated.append(get_translated_object(vehicle))
    
    headers = False
    for vehicle in vehicles_translated:
        if not headers:
            csv_writer.writerow(vehicle.keys())
            headers = True
        csv_writer.writerow(vehicle.values())
        
    return response


# Refresh vehicle list with Firebase
def refresh(request, type):
    database = get_database()
    if database is None:
        return redirect('/vehicles/' + type)
    source = request.POST['source']
    if source == 'local': 
        vehicles_local = Vehicle.objects.all().order_by('id')
        database.child('Catalog/Vehicles').remove()
        for vehicle in vehicles_local:
            translated_vehicle = get_translated_object(vehicle)
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
                    range=vehicle.range,
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