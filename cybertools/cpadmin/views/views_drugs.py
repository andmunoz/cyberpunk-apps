from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, Brand, Availability, DrugType, Drug
)
from cpadmin.config import database


# Show drug list
def list(request):
    drugs = Drug.objects.all().order_by('name')
    drug_count = 0
    if drugs:
        drug_count = len(drugs)

    categories = Category.objects.filter(type='DRUGS').order_by('name')
    brands = Brand.objects.filter(type='DRUGS').order_by('name')
    availabilities = Availability.choices
    drug_types = DrugType.choices

    context = {
        'page_title': 'Drogas',
        'drugs_count': drug_count,
        'drugs': drugs,
        'categories': categories,
        'brands': brands,
        'availabilities': availabilities,
        'drugs_types': drug_types,
    }
        
    return render(request, 'drugs/drug.html', context)


# Create an drug
def create(request):
    form = request.POST
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    drug = Drug(
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
    drug.save()

    return redirect('drug')


# Update an drug
def update(request):
    form = request.POST
    drug = Drug.objects.get(id=form['id'])
    category = Category.objects.get(id=form['category'])
    brand = Brand.objects.get(id=form['brand'])
    drug.name = form['name']
    drug.category = category
    drug.brand = brand
    drug.type = form['type']
    drug.weight = float(form['weight'])
    drug.cost = int(form['cost'])
    drug.description = form['description']
    drug.image = form['image']
    drug.save()
    
    return redirect('drug')


# Delete an drug
def delete(request):
    form = request.POST
    drug = Drug.objects.get(id=form['id'])
    drug.delete()
    return redirect('drug')


# Upload drug list from CSV
def upload(request):
    csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        category = Category.objects.get(name=row['category'], type=ItemType.DRUGS, parent=None)
        brand, _ = Brand.objects.get_or_create(
            name=row['brand'], type=ItemType.DRUGS,
            defaults={'name': row['brand'], 'type': ItemType.DRUGS, 'description': 'Autogenerated'})

        Drug.objects.update_or_create(
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
        
    return redirect('drug')


# Download drug list in CSV
def download(request):
    drugs = Drug.objects.all().order_by('name').values()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="drugs.csv"'
    csv_writer = csv.writer(response)
    headers = False

    drugs_translated = []
    for drug in drugs:
        drug_translated = {}
        keys = drug.keys()
        for key in keys:
            value = drug[key]
            if key == 'category_id':
                category = Category.objects.get(id=value)
                drug_translated['category'] = category.code
            elif key == 'brand_id': 
                brand = Brand.objects.get(id=value)
                drug_translated['brand'] = brand.name
            else:
                drug_translated[key] = value
        drugs_translated.append(drug_translated)
    
    for drug in drugs_translated:
        if not headers:
            csv_writer.writerow(drug.keys())
            headers = True
        csv_writer.writerow(drug.values())
        
    return response


# Refresh drug list with Firebase
def refresh(request):
    source = request.POST['source']
    if source == 'local': 
        drug_local = Drug.objects.all().order_by('id').values()
        database.child('Catalog/Drug').remove()
        for drug in drug_local:
            database.child('Catalog/Drug').push(drug)
    else:
        drug_origin = database.child('Catalog/Drug').get()
        for drug_id, drug in drug_origin:
            category = Category.objects.get(code=drug.category, parent=None)
            brand, _ = Brand.objects.get_or_create(
                name=drug.brand, 
                defaults={'name': drug.brand, 'type': ItemType.DRUGS, 'description': 'Autogenerated'})
            
            Drug.objects.update_or_create(
                id=drug_id,
                defaults=dict(
                    name=drug.name,
                    category=category,
                    brand=brand,
                    availability=drug.availability,
                    type=drug.type,
                    weight=drug.weight,
                    cost=drug.cost,
                    description=drug.description,
                    image=drug.image,
                ),
            )

    return redirect('drug')
