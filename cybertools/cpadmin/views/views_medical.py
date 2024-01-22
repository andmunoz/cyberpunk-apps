from django.shortcuts import render, redirect, HttpResponse
import csv
from cpadmin.models import (
    ItemType, Category, Brand, Availability, Medical
)
from cpadmin.config import get_database, get_type, get_translated_object, download_csv


# Show medical list
def list(request):
    medicals = Medical.objects.all().order_by('name')
    medical_count = 0
    if medicals:
        medical_count = len(medicals)

    medical_types = Medical.Type.choices
    medical_qualities = Medical.Quality.choices

    context = {
        'page_title': 'Cuidados Médicos',
        'medical_count': medical_count,
        'medicals': medicals,
        'medical_types': medical_types,
        'medical_qualities': medical_qualities,
    }
        
    return render(request, 'drugs/medical.html', context)


# Create an medical
def create(request):
    form = request.POST
    medical = Medical(
        name=form['name'],
        type=form['type'],
        quality=form['quality'],
        elapsed_time=form['elapsed_time'],
        elapsed_time_uom=form['elapsed_time_uom'],
        cost=int(form['cost']),
        description=form['description'],
    )
    medical.save()

    return redirect('medical')


# Update an medical
def update(request):
    form = request.POST
    medical = Medical.objects.get(id=form['id'])
    medical.name = form['name']
    medical.type = form['type']
    medical.quality = form['quality'],
    medical.elapsed_time = form['elapsed_time'],
    medical.elapsed_time_uom = form['elapsed_time_uom'],
    medical.cost = int(form['cost'])
    medical.description = form['description']
    medical.save()
    
    return redirect('medical')


# Delete an medical
def delete(request):
    form = request.POST
    medical = Medical.objects.get(id=form['id'])
    medical.delete()
    return redirect('medical')


# Upload medical list from CSV
def upload(request):
    csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        Medical.objects.update_or_create(
            id=row['id'],
            defaults=dict(
                name=row['name'],
                type=row['type'],
                quality=row['quality'],
                elapsed_time=row['elapsed_time'],
                elapsed_time_uom=row['elapsed_time_uom'],
                cost=int(row['cost']),
                description=row['description'],
                image=row['image'],
            )
        )
        
    return redirect('medical')


# Download medical list in CSV
def download(request):
    medicals = Medical.objects.all().order_by('name').values()
    return download_csv(Medical, medicals)


# Refresh medical list with Firebase
def refresh(request):
    database = get_database()
    if database is None:
        return redirect('medical') 
    source = request.POST['source']
    if source == 'local': 
        medical_local = Medical.objects.all().order_by('id').values()
        database.child('Lifestyle/Medical').remove()
        for medical in medical_local:
            database.child('Lifestyle/Medical').push(medical)
    else:
        medical_origin = database.child('Lifestyle/Medical').get()
        for medical_id, medical in medical_origin:
            Medical.objects.update_or_create(
                id=medical_id,
                defaults=dict(
                    name=medical.name,
                    type=medical.type,
                    quality=medical.quality,
                    elapsed_time=medical.elapsed_time,
                    elapsed_time_uom=medical.elapsed_time_uom,
                    cost=medical.cost,
                    description=medical.description,
                    image=medical.image,
                ),
            )

    return redirect('medical')
