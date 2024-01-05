from django.shortcuts import render, redirect, HttpResponse
import csv
from .models import (
    ItemType, Gear, Category, Brand, Availability, GearType
)
from .config import database


# Show gear list
def list(request):
    gears = Gear.objects.all().order_by('name')
    gear_count = 0
    if gears:
        gear_count = len(gears)

    categories = Category.objects.filter(type='GEAR').order_by('name')
    brands = Brand.objects.filter(type='GEAR').order_by('name')
    availabilities = Availability.choices
    gear_types = GearType.choices

    context = {
        'page_title': 'Equipo',
        'gear_count': gear_count,
        'gears': gears,
        'categories': categories,
        'brands': brands,
        'availabilities': availabilities,
        'gear_types': gear_types,
    }
        
    return render(request, 'equipment/gear.html', context)


# Create an gear
def create(request):
    form = request.POST
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    gear = Gear(
        name=form['name'],
        category=category,
        brand=brand,
        availability=form['availability'],
        type=form['type'],
        weight=float(form['weight']),
        cost=int(form['cost']),
        description=form['description'],
        image=form['image'],
    )
    gear.save()

    return redirect('gear')


# Update an gear
def update(request):
    form = request.POST
    gear = Gear.objects.get(id=form['id'])
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    gear.name = form['name']
    gear.category = category
    gear.brand = brand
    gear.type = form['type']
    gear.weight = float(form['weight'])
    gear.cost = int(form['cost'])
    gear.description = form['description']
    gear.image = form['image']
    gear.save()
    
    return redirect('gear')


# Delete an gear
def delete(request):
    form = request.POST
    gear = Gear.objects.get(id=form['id'])
    gear.delete()
    return redirect('gear')


# Upload gear list from CSV
def upload(request):
    csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        category = Category.objects.get(name=row['category'], parent=None)
        brand, _ = Brand.objects.get_or_create(
            name=row['brand'], type=ItemType.GEAR,
            defaults={'name': row['brand'], 'type': ItemType.GEAR, 'description': 'Autogenerated'})

        Gear.objects.update_or_create(
            id=row['id'],
            defaults=dict(
                name=row['name'],
                category=category,
                brand=brand,
                availability=row['availability'],
                type=row['type'],
                weight=float(row['weight']),
                cost=int(row['cost']),
                description=row['description'],
                image=row['image'],
            )
        )
        
    return redirect('gear')


# Download gear list in CSV
def download(request):
    gears = Gear.objects.all().order_by('name').values()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gears.csv"'
    csv_writer = csv.writer(response)
    headers = False

    gears_translated = []
    for gear in gears:
        gear_translated = {}
        keys = gear.keys()
        for key in keys:
            value = gear[key]
            if key == 'category_id':
                category = Category.objects.get(id=value)
                gear_translated['category'] = category.code
            elif key == 'brand_id': 
                brand = Brand.objects.get(id=value)
                gear_translated['brand'] = brand.name
            else:
                gear_translated[key] = value
        gears_translated.append(gear_translated)
    
    for gear in gears_translated:
        if not headers:
            csv_writer.writerow(gear.keys())
            headers = True
        csv_writer.writerow(gear.values())
        
    return response


# Refresh gear list with Firebase
def refresh(request):
    source = request.POST['source']
    if source == 'local': 
        gear_local = Gear.objects.all().order_by('id').values()
        database.child('Catalog/Gear').remove()
        for gear in gear_local:
            database.child('Catalog/Gear').push(gear)
    else:
        gear_origin = database.child('Catalog/Gear').get()
        for gear_id, gear in gear_origin:
            category = Category.objects.get(code=gear.category, parent=None)
            brand, _ = Brand.objects.get_or_create(
                name=gear.brand, 
                defaults={'name': gear.brand, 'type': ItemType.GEAR, 'description': 'Autogenerated'})
            
            Gear.objects.update_or_create(
                id=gear_id,
                defaults=dict(
                    name=gear.name,
                    category=category,
                    brand=brand,
                    availability=gear.availability,
                    type=gear.type,
                    weight=gear.weight,
                    cost=gear.cost,
                    description=gear.description,
                    image=gear.image,
                ),
            )

    return redirect('gear')
