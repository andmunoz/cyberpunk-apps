from django.contrib import admin
from cpadmin.models.models import Category, CategoryAdmin, Brand, BrandAdmin, Surgery, SurgeryAdmin
from cpadmin.models.models_weapon import Weapon, WeaponAdmin
from cpadmin.models.models_armor import Armor, ArmorAdmin
from cpadmin.models.models_gear import Gear, GearAdmin
from cpadmin.models.models_cyberware import Cyberware, CyberwareAdmin
from cpadmin.models.models_clothes import Clothes, ClothesAdmin
from cpadmin.models.models_drugs import Drug, DrugAdmin, DrugEffect, DrugEffectAdmin, DrugSideEffect, DrugSideEffectAdmin
from cpadmin.models.models_medical import Medical, MedicalAdmin
from cpadmin.models.models_vehicle import Vehicle, VehicleAdmin

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Surgery, SurgeryAdmin)
admin.site.register(Cyberware, CyberwareAdmin)
admin.site.register(Clothes, ClothesAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(DrugEffect, DrugEffectAdmin)
admin.site.register(DrugSideEffect, DrugSideEffectAdmin)
admin.site.register(Medical, MedicalAdmin)
admin.site.register(Vehicle, VehicleAdmin)
