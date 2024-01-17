from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, 
    DrugType, DrugLegality, DrugForm, DrugEffect, DrugSideEffect, DrugAddiction, Drug
)
from cpadmin.config import get_database


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
        overdose_description=form['overdose_description'],
        addiction=form['addiction'],
        next_dose=form['next_dose'],
        symptoms=form['symptoms'],
        cost=int(form['cost']),
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
    drug.name = form['name']
    drug.category = category
    drug.type = form['type']
    drug.legality=form['legality']
    drug.form=form['form']
    drug.dosis=form['dosis']
    drug.presentation=form['presentation']
    drug.strength=int(form['strength'])
    drug.speed=form['speed']
    drug.effects_description=form['effects_description']
    drug.side_effects_description=form['side_effects_description']
    drug.duration=form['duration']
    drug.overdose_description=form['overdose_description'],
    drug.addiction=form['addiction']
    drug.next_dose=form['next_dose']
    drug.symptoms=form['symptoms']
    drug.cost = int(form['cost'])
    drug.description = form['description']
    
    selected_effects = DrugEffect.objects.filter(id__in=form.getlist('effects'))
    drug.effects.set(selected_effects)
    selected_side_effects = DrugSideEffect.objects.filter(id__in=form.getlist('side_effects'))
    drug.side_effects.set(selected_side_effects)

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
        selected_effects = row['effects'].split(",")
        effects = []
        for effect in selected_effects:
            effects.append(effect)
        selected_side_effects = row['side_effects'].split(",")
        side_effects = []
        for side_effect in selected_side_effects:
            side_effects.append(side_effect)
            
        drug, created = Drug.objects.update_or_create(
            id=row['id'],
            defaults=dict(
                name=row['name'],
                category=category,
                type=row['type'],
                legality=row['legality'],
                form=row['form'],
                dosis=row['dosis'],
                presentation=row['presentation'],
                strength=int(row['strength']),
                speed=row['speed'],
                effects_description=row['effects_description'],
                side_effects_description=row['side_effects_description'],
                overdose_description=row['overdose_description'],
                duration=row['duration'],
                addiction=row['addiction'],
                next_dose=row['next_dose'],
                symptoms=row['symptoms'],
                cost=int(row['cost']),
                description=row['description'],
            )
        )

        selected_effects = row['effects'].split(",")
        effects_list = []
        for effect in selected_effects:
            effects_list.append(effect)
        effects = DrugEffect.objects.filter(name__in=effects_list)
        drug.effects.set(effects)
            
        selected_side_effects = row['side_effects'].split(",")
        side_effects_list = []
        for side_effect in selected_side_effects:
            side_effects_list.append(side_effect)
        side_effects = DrugSideEffect.objects.filter(name__in=side_effects_list)
        drug.side_effects.set(side_effects)
        
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
            print(key)
            if key == 'category_id':
                category = Category.objects.get(id=value)
                drug_translated['category'] = category.code
            else:
                drug_translated[key] = value
        drugs_translated.append(drug_translated)
    
    # TODO: put effect and side effects list in csv
    
    for drug in drugs_translated:
        if not headers:
            csv_writer.writerow(drug.keys())
            headers = True
        csv_writer.writerow(drug.values())
        
    return response


# Refresh drug list with Firebase
def refresh(request):
    database = get_database()
    if database is None:
        return redirect('drugs') 
    source = request.POST['source']
    if source == 'local': 
        drug_local = Drug.objects.all().order_by('id').values()
        database.child('Catalog/Drugs').remove()
        for drug in drug_local:
            database.child('Catalog/Drugs').push(drug)
    else:
        drug_origin = database.child('Catalog/Drug').get()
        for drug_id, drug in drug_origin:
            category = Category.objects.get(code=drug.category, parent=None)
            
            Drug.objects.update_or_create(
                id=drug_id,
                defaults=dict(
                    name=drug.name,
                    category=category,
                    type=drug.type,
                    legality=drug.legality,
                    form=drug.form,
                    dosis=drug.dosis,
                    presentation=drug.presentation,
                    strength=int(drug.strength),
                    speed=drug.speed,
                    effects_description=drug.effects_description,
                    side_effects_description=drug.side_effects_description,
                    duration=drug.duration,
                    overdose_description=drug.overdose_description,
                    addiction=drug.addiction,
                    next_dose=drug.next_dose,
                    symptoms=drug.symptoms,
                    cost=drug.cost,
                    description=drug.description,
                ),
            )
            
            # TODO: put effect and side effects list in object

    return redirect('drugs')
