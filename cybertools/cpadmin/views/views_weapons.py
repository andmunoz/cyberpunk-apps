from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, Brand, Availability, WeaponConcealment, WeaponReliability, Weapon
)
from cpadmin.config import database


# Show weapon List
def list(request):
    weapons = Weapon.objects.all().order_by('name')
    weapons_count = 0
    if weapons:
        weapons_count = len(weapons)

    categories = Category.objects.filter(type='WEAPON').order_by('name')
    brands = Brand.objects.filter(type='WEAPON').order_by('name')
    availabilities = Availability.choices
    concealments = WeaponConcealment.choices
    reliabilities = WeaponReliability.choices

    context = {
        'page_title': 'Armas',
        'weapons_count': weapons_count,
        'weapons': weapons,
        'categories': categories,
        'brands': brands,
        'availabilities': availabilities,
        'concealments': concealments,
        'reliabilities': reliabilities,
    }
        
    return render(request, 'equipment/weapons.html', context)


# Create a weapon
def create(request):
    form = request.POST
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    weapon = Weapon(
        name=form['name'],
        category=category,
        brand=brand,
        availability=form['availability'],
        concealment=form['concealment'],
        accuracy=form['accuracy'],
        reliability=form['reliability'],
        range=float(form['range']) if form['range'] != '' else None,
        shots=int(form['shots']) if form['shots'] != '' else None,
        rof=int(form['rof']) if form['rof'] != '' else None,
        damage=form['damage'],
        weight=float(form['weight']),
        cost=int(form['cost']),
        description=form['description'],
        image=form['image'],
    )
    weapon.save()

    return redirect('weapons')


# Update a weapon
def update(request):
    form = request.POST
    weapon = Weapon.objects.get(id=form['id'])
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    weapon.name = form['name']
    weapon.category = category
    weapon.brand = brand
    weapon.availability = form['availability']
    weapon.concealment = form['concealment']
    weapon.accuracy = form['accuracy']
    weapon.reliability = form['reliability']
    weapon.range = float(form['range']) if form['range'] != '' else None
    weapon.shots = int(form['shots']) if form['shots'] != '' else None
    weapon.rof = int(form['rof']) if form['rof'] != '' else None
    weapon.damage = form['damage']
    weapon.weight = float(form['weight'])
    weapon.cost = int(form['cost'])
    weapon.description = form['description']
    weapon.image = form['image']
    weapon.save()

    return redirect('weapons')


# Delete a weapon
def delete(request):
    form = request.POST
    weapon = Weapon.objects.get(id=form['id'])
    weapon.delete()

    return redirect('weapons')

# Upload weapons list from CSV
def upload(request):
    csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        category = Category.objects.get(code=row['category'], parent=None)
        brand, _ = Brand.objects.get_or_create(
            name=row['brand'], 
            defaults={'name': row['brand'], 'type': ItemType.WEAPON, 'description': 'Autogenerated'})

        Weapon.objects.update_or_create(
            id=row['id'],
            defaults=dict(
                name=row['name'],
                category=category,
                brand=brand,
                availability=row['availability'],
                concealment=row['concealment'],
                accuracy=row['accuracy'],
                reliability=row['reliability'],
                range=float(row['range']) if row['range'] != '' else None,
                shots=int(row['shots']) if row['shots'] != '' else None,
                rof=int(row['rof']) if row['rof'] != '' else None,
                damage=row['damage'],
                weight=float(row['weight']),
                cost=int(row['cost']),
                description=row['description'],
                image=row['image'],
            )
        )

    return redirect('weapons')


# Download weapon list in CSV
def download(request):
    weapons = Weapon.objects.all().order_by('name').values()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="weapons.csv"'
    csv_writer = csv.writer(response)
    headers = False

    weapons_translated = []
    for weapon in weapons:
        weapon_translated = {}
        keys = weapon.keys()
        for key in keys:
            value = weapon[key]
            if key == 'category_id':
                category = Category.objects.get(id=value)
                weapon_translated['category'] = category.code
            elif key == 'brand_id': 
                brand = Brand.objects.get(id=value)
                weapon_translated['brand'] = brand.name
            else:
                weapon_translated[key] = value
        weapons_translated.append(weapon_translated)
    
    for weapon in weapons_translated:
        if not headers:
            csv_writer.writerow(weapon.keys())
            headers = True
        csv_writer.writerow(weapon.values())
        
    return response


# Refresh weapons list with Firebase
def refresh(request):
    source = request.POST['source']
    if source == 'local': 
        weapons_local = Weapon.objects.all().order_by('id').values()
        database.child('Catalog/Weapon').remove()
        for weapon in weapons_local:
            database.child('Catalog/Weapon').push(weapon)
    else:
        weapons_origin = database.child('Catalog/Weapon').get()
        for weapon_id, weapon in weapons_origin:
            category = Category.objects.get(code=weapon.category, type=ItemType.WEAPON, parent=None)
            brand, _ = Brand.objects.get_or_create(
                name=weapon.brand, type=ItemType.WEAPON,
                defaults={'name': weapon.brand, 'type': ItemType.WEAPON, 'description': 'Autogenerated'})
            
            Weapon.objects.update_or_create(
                id=weapon_id,
                defaults=dict(
                    name=weapon.name,
                    category=category,
                    brand=brand,
                    availability=weapon.availability,
                    concealment=weapon.concealment,
                    accuracy=weapon.accuracy,
                    reliability=weapon.realiability,
                    range=weapon.range,
                    shots=weapon.shots,
                    rof=weapon.rof,
                    damage=weapon.damage,
                    weight=weapon.weight,
                    cost=weapon.cost,
                    description=weapon.description,
                    image=weapon.image,
                ),
            )
            
    return redirect('weapons')