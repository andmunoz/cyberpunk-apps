from django.shortcuts import HttpResponse
import csv, collections.abc, collections
collections.MutableMapping = collections.abc.MutableMapping
collections.Mapping = collections.abc.Mapping
import pyrebase
from .models import Category, Brand, Availability, Surgery, TimeUOM

# Firebase Configurations
config = {
    "apiKey": "AIzaSyD3LUVINjIt9XAHvMZyXojbqGv-EXrKeUk",
    "authDomain": "cyberpunk-database.firebaseapp.com",
    "databaseURL": "https://cyberpunk-database.firebaseio.com",
    "projectId": "cyberpunk-database",
    "storageBucket": "cyberpunk-database.appspot.com",
    "messagingSenderId": "492371389033",
    "appId": "1:492371389033:web:03dc0c1000b49c6b5350f8",
    "measurementId": "G-FRRFLZ6T17",
    "token": "",
}

# Data user authentication
email = "andmunoz@gmail.com"
password = ".La441219"

# Pyrebase initialization
def get_database():
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print("Authenticated user: ", user['email'])
    except Exception as e:
        print("Authtentication Error: ", e)
        
    return firebase.database()


# Get id of a Type Choice
def get_type(choice_object, key=None, value=None):
    if value: 
        return choice_object[value.upper()]
    else:
        for choice_code, display_value in choice_object.choices:
            if choice_code == key:
                return display_value
    return None


# Get humanized dictionary from Object
def get_translated_object(Model, object):
    object_translated = dict()
    for key in object.keys():
        if key == "category_id":
            category = Category.objects.get(id=object[key])
            object_translated[Model._meta.get_field(key).verbose_name] = category.name
        elif key == "brand_id":
            brand = Brand.objects.get(id=object[key])
            object_translated[Model._meta.get_field(key).verbose_name] = brand.name
        elif key == "type":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Type, key=object[key])
        elif key == "availability":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Availability, key=object[key])
        elif key == "concealment":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Concealment, key=object[key])
        elif key == "reliability":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Reliability, key=object[key])
        elif key == "coverage":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Coverage, key=object[key])
        elif key == "slot":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Slot, key=object[key])
        elif key == "surgery_id":
            surgery = Surgery.objects.get(id=object[key])
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Surgery.Type, key=surgery.type)
        elif key == "form":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Form, key=object[key])
        elif key == "legality":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Legality, key=object[key])
        elif key == "addiction":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Addiction, key=object[key])
        elif key == "quality":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Quality, key=object[key])
        elif key == "elapsed_time_uom":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(TimeUOM, key=object[key])
        elif key == "top_speed":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " km/hr" if object[key] else ""
        elif key == "acceleration" or key == "deceleration":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " m/s" if object[key] else ""
        elif key == "range":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " m" if object[key] else ""
        elif key == "autonomy":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " kms" if object[key] else ""
        elif key == "cargo" or key == 'weight':
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " kgs" if object[key] else ""
        elif key == "cost":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " creds" if object[key] else ""
        else: 
            object_translated[Model._meta.get_field(key).verbose_name] = object[key] if object[key] else ""
    return object_translated


# Get translated list of objects
def download_csv(Model, objects):
    filename = Model._meta.model_name
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'
    csv_writer = csv.writer(response)

    headers = False
    for object in objects.values():
        translated_object = get_translated_object(Model, object)
        if not headers:
            csv_writer.writerow(translated_object.keys())
            headers = True
        csv_writer.writerow(translated_object.values())

    return response
