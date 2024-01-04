from django.contrib import admin
from .models import (
    Category, CategoryAdmin, 
    Brand, BrandAdmin,
    Weapon, WeaponAdmin,
    Armor, ArmorAdmin, 
    Gear, GearAdmin, 
    Surgery, SurgeryAdmin,
    Cyberware, CyberwareAdmin
)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Surgery, SurgeryAdmin)
admin.site.register(Cyberware, CyberwareAdmin)
