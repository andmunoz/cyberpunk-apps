from django.contrib import admin
from cpadmin.models import (
    Category, CategoryAdmin, 
    Brand, BrandAdmin,
    Weapon, WeaponAdmin,
    Armor, ArmorAdmin, 
    Gear, GearAdmin, 
    Surgery, SurgeryAdmin,
    Cyberware, CyberwareAdmin,
    Clothes, ClothesAdmin, 
    Drug, DrugEffect, DrugSideEffect, DrugAdmin,
    Medical, MedicalAdmin, 
    Vehicle, VehicleAdmin,
)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Surgery, SurgeryAdmin)
admin.site.register(Cyberware, CyberwareAdmin)
admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(DrugEffect)
admin.site.register(DrugSideEffect)
admin.site.register(Medical, MedicalAdmin)
admin.site.register(Vehicle, VehicleAdmin)
