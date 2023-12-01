from ninja import NinjaAPI, Swagger, Redoc
from cpadmin.models import Weapon, Category, Brand

api = NinjaAPI(docs=Redoc())


# Endpoints and utilities for weapons
def weapon_to_json(weapon):
    data = {
        'id': weapon.id,
        'name': weapon.name,
        'category': weapon.category.name,
        'brand': weapon.brand.name,
        'availability': weapon.availability,
        'accuracy': weapon.accuracy,
        'concealment': weapon.concealment,
        'realibility': weapon.reliability,
        'shots': weapon.shots,
        'rof': weapon.rof,
        'range': weapon.range,
        'weight': weapon.weight,
        'cost': weapon.cost,
    }
    return data


@api.get("/weapon")
def get_weapons(request):
    weapons = Weapon.objects.all().order_by("name")
    data = []
    for weapon in weapons:
        data.append(weapon_to_json(weapon))
    return data


@api.get("/weapon/{id}")
def get_weapon(request, id):
    weapon = Weapon.objects.get(id=id)
    return weapon_to_json(weapon=weapon)


# Endpoints and utilities for weapon categories
def category_to_json(category):
    data = {
        'id': category.id,
        'name': category.name,
        'code': category.code,
        'description': category.description,
    }
    return data


@api.get("/category")
def get_categories(request):
    categories = Category.objects.all().order_by("name")
    data = []
    for category in categories:
        data.append(category_to_json(category))
    return data


# Endpoints and utilities for weapon brands
def brand_to_json(brand):
    data = {
        'id': brand.id,
        'name': brand.name,
        'description': brand.description,
    }
    return data


# Endpoints and utilities for weapon brands
@api.get("/brand")
def get_brands(request):
    brands = Brand.objects.all().order_by("name")
    data = []
    for brand in brands:
        data.append(brand_to_json(brand))
    return data
