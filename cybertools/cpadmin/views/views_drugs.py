from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, Brand, 
    DrugType, DrugLegality, DrugForm, DrugEffect, DrugSideEffect, DrugAddiction, Drug
)
from cpadmin.config import database


# Show drug list
def list(request):
    drugs = Drug.objects.all().order_by('name')
    drug_count = 0
    if drugs:
        drug_count = len(drugs)

    categories = Category.objects.filter(type='DRUGS').order_by('name')
    drug_types = DrugType.choices
    drug_legalities = DrugLegality.choices
    drug_forms = DrugForm.choices
    drug_effects = DrugEffect.objects.all().order_by('name')
    drug_side_effects = DrugSideEffect.objects.all().order_by('name')
    drug_addictions = DrugAddiction.choices

    context = {
        'page_title': 'Drogas',
        'drugs_count': drug_count,
        'drugs': drugs,
        'categories': categories,
        'drugs_types': drug_types,
        'drug_legalities': drug_legalities,
        'drug_forms': drug_forms,
        'drug_effects': drug_effects,
        'drug_side_effects': drug_side_effects,
        'drug_addictions': drug_addictions,
    }
        
    return render(request, 'drugs/drug.html', context)


# Create an drug
def create(request):
    form = request.POST
    category = Category.objects.get(id=form['category'])
    
    drug = Drug(
        name=form['name'],
        category=category,
        type=form['type'],
        legality=form['legality'],
        form=form['form'],
        dosis=form['dosis'],
        presentation=form['presentation'],
        strength=int(form['strength']),
        speed=form['speed'],
        effects_description=form['effects_description'],
        side_effects_description=form['side_effects_description'],
        duration=form['duration'],
        addiction=form['addiction'],
        next_dose=form['next_dose'],
        symptoms=form['symptoms'],
        cost=int(form['cost']),
        overdose_description=form['overdose_description'],
        description=form['description'],
    )
    drug.save()

    selected_effects = DrugEffect.objects.filter(id__in=form.getlist('effects'))
    drug.effects.set(selected_effects)
    selected_side_effects = DrugSideEffect.objects.filter(id__in=form.getlist('side_effects'))
    drug.side_effects.set(selected_side_effects)

    return redirect('drugs')


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
    drug.save()
    
    return redirect('drugs')


# Delete an drug
def delete(request):
    form = request.POST
    drug = Drug.objects.get(id=form['id'])
    drug.delete()
    return redirect('drugs')


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
            )
        )
        
    return redirect('drugs')


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
                ),
            )

    return redirect('drugs')
