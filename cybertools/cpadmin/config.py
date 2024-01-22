import collections.abc
import collections
collections.MutableMapping = collections.abc.MutableMapping
collections.Mapping = collections.abc.Mapping
import pyrebase
from .models import Category, Brand

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
    object_translated = {}
    for key in object.keys():
        if key == "category_id":
            category = Category.objects.get(id=object["category_id"])
            object_translated[Model._meta.get_field(key).verbose_name] = category.name
        elif key == "brand_id":
            brand = Brand.objects.get(id=object["brand_id"])
            object_translated[Model._meta.get_field(key).verbose_name] = brand.name
        elif key == "type":
            object_translated[Model._meta.get_field(key).verbose_name] = get_type(Model.Type, key=object[key])
        elif key == "top_speed":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " km/hr"
        elif key == "acceleration" or key == "deceleration":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " m/s"
        elif key == "range":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " m"
        elif key == "autonomy":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " kms"
        elif key == "cargo" or key == 'weight':
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " kgs"
        elif key == "cost":
            object_translated[Model._meta.get_field(key).verbose_name] = "{:,}".format(object[key]) + " creds"
        else: 
            object_translated[Model._meta.get_field(key).verbose_name] = object[key]
    return object_translated
