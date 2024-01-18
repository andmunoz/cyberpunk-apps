from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


### General Models
class ItemType(models.TextChoices):
    WEAPON = 'WEAPON', _('Armas')
    ARMOR = 'ARMOR', _('Blindaje')
    GEAR = 'GEAR', _('Equipo')
    CYBER = 'CYBER', _('Ciberequipo')
    CLOTHES = 'CLOTHES', _('Moda')
    DRUGS = 'DRUGS', _('Drogas')
    MEDICAL = 'MEDICAL', _('Cuidados Médicos')
    VEHICLE = 'VEHICLE', _('Vehículos')
    HARDWARE = 'HARDWARE', _('Periféricos')
    SOFTWARE = 'SOFTWARE', _('Programas')


class Category(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, blank=True)
    type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.WEAPON)
    description = models.CharField(max_length=1000, blank=True)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "type", "parent"]
    
    
class Brand(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.WEAPON)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    
    
class Availability(models.TextChoices): 
    EXCELLENT = 'E', _('Excelente')
    COMMON = 'C', _('Común')
    POOR = 'P', _('Mala')
    RARE = 'R', _('Rara')
    ARMY = 'A', _('Solo Militares')
    EXPERIMENTAL = 'X', _('Experimental')
   

class TimeUOM(models.TextChoices): 
    SECONDS = 'SEC', _('Segundos')
    MINUTES = 'MIN', _('Minutos')
    HOURS = 'HRS', _('Horas')
    DAYS = 'D', _('Días')
    WEEKS = 'W', _('Semanas')
    MONTHS = 'M', _('Meses')
    QUARTERS = 'Q', _('Trimestres')
    YEARS = 'Y', _('Años')
   

### Specific Models for Weapons
class WeaponConcealment(models.TextChoices): 
    POCKET = 'P', _('Bolsillo')
    JACKET = 'J', _('Chaqueta')
    LONG = 'L', _('Chaqueta Larga')
    NONE = 'N', _('No')
   

class WeaponReliability(models.TextChoices): 
    VERY = 'VR', _('Muy Fiable')
    STANDARD = 'ST', _('Fiable')
    UNREL = 'UR', _('Poco Fiable')
   
    
class Weapon(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    accuracy = models.IntegerField()
    concealment = models.CharField(max_length=2, choices=WeaponConcealment.choices, default=WeaponConcealment.JACKET)
    reliability = models.CharField(max_length=2, choices=WeaponReliability.choices, default=WeaponReliability.STANDARD)
    shots = models.IntegerField(blank=True, null=True)
    rof = models.IntegerField(blank=True, null=True)
    range = models.IntegerField(blank=True, null=True)
    damage = models.CharField(max_length=20)
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name


class WeaponAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "concealment", "reliability", "availability", "cost"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.WEAPON)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.WEAPON)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
### Specific Models for Armor
class ArmorCoverage(models.TextChoices): 
    HEAD = 'HEAD', _('Cabeza')
    TORSO = 'TORSO', _('Torso')
    UPPER = 'UPPER', _('Torso y Brazos')
    LOWER = 'LOWER', _('Piernas')
    BODY = 'BODY', _('Cuerpo')
    FULL = 'FULL', _('Todo')


class ArmorType(models.TextChoices): 
    SOFT = 'S', _('Blando')
    HARD = 'H', _('Duro')       
  
    
class Armor(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    coverage = models.CharField(max_length=20, choices=ArmorCoverage.choices, default=ArmorCoverage.BODY)
    type = models.CharField(max_length=1, choices=ArmorType.choices, default=ArmorType.HARD)
    sp = models.IntegerField()
    ev = models.IntegerField()
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name


class ArmorAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "type", "coverage", "availability", "cost"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.ARMOR)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.ARMOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Gear
class GearType(models.TextChoices): 
    OPTIONAL = 'OPT', _('Opcional')


class Gear(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    type = models.CharField(max_length=3, choices=GearType.choices, default=GearType.OPTIONAL)
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class GearAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "type", "availability", "cost"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.GEAR)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.GEAR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Surgery
class SurgeryTypes(models.TextChoices): 
    NO = 'NO', _('No Aplica')
    INSIGNIFICANT = 'IN', _('Insignificante')
    SECONDARY = 'SE', _('Secundaria')
    IMPORTANT = 'IM', _('Importante')
    CRITICAL = 'CR', _('Crítica')

class Surgery(models.Model):
    type = models.CharField(max_length=2, choices=SurgeryTypes.choices)
    difficulty = models.IntegerField()
    time_length = models.IntegerField()
    damage = models.CharField(max_length=10, default='No')
    cost = models.BigIntegerField(default=0)

    def __str__(self):
        return self.get_type_display()


class SurgeryAdmin(admin.ModelAdmin):
    list_display = ["type", "difficulty", "time_length", "damage", "cost"]
    

### Specific Models for Cyberware
class CyberType(models.TextChoices): 
    IMPLANT = 'IMP', _('Implante')
    EXTERNAL = 'EXT', _('Externo')
    ADDON = 'ADD', _('Opción')
    IMPROVEMENT = 'IMPRO', _('Mejora')
    MRAM = 'MRAM', _('Chip de Memoria')
    CPART = 'CPART', _('Chip de Reflejos')


class CyberSlot(models.TextChoices):
    FULL = 'FUL', _('Cuerpo y Cabeza')
    HEAD = 'HEA', _('Cabeza')
    BODY = 'BOD', _('Cuerpo')
    TORSO = 'TOR', _('Torso')
    ARM = 'ARM', _('Brazo')
    ARMLEG = 'AOL', _('Brazo o Pierna')
    LEG = 'LEG', _('Pierna')
    CROTCH = 'CRO', _('Ingle')
    

class Cyberware(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    type = models.CharField(max_length=5, choices=CyberType.choices, default=CyberType.IMPLANT)
    humanity = models.CharField(max_length=10, null=True)
    requirement = models.CharField(max_length=100, null=True, blank=True)
    adjustment = models.CharField(max_length=100, null=True, blank=True)
    slot = models.CharField(max_length=3, choices=CyberSlot.choices, default=CyberSlot.FULL)
    surgery = models.ForeignKey("Surgery", on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class CyberwareAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "type", "humanity", "slot", "adjustment", "requirement", "surgery", "availability", "cost"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.CYBER)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.CYBER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Clothes
class ClothesType(models.TextChoices): 
    UNISEX = 'U', _('Unisex')
    MALE = 'M', _('Masculino')
    FEMALE = 'F', _('Femenino')
    NO = 'N', _('Sin Tipo')


class Clothes(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    type = models.CharField(max_length=3, choices=ClothesType.choices, default=ClothesType.NO)
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class ClothesAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "type", "availability", "cost"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.CLOTHES)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.CLOTHES)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Drugs
class DrugType(models.TextChoices): 
    BEVERAGE = 'B', _('Bebidas Alcohólicas')
    CIGARRETTE = 'C', _('Cigarrillos')
    MEDICINE = 'M', _('Fármaco')
    DRUG = 'D', _('Droga')


class DrugForm(models.TextChoices):
    PILL = 'P', _('Píldora o Tableta')
    GELCAP = 'G', _('Cápsula')
    PAPER = 'T', _('Pestaña de Papel')
    SMOKE = 'S', _('Fumado, Inhalado')
    POWDER = 'PI', _('En polvo, Inhalado')
    INJECTED = 'I', _('Inyectado')
    LIQUID = 'L', _('Líquido')
    BAND = 'B', _('Parche')
    CONTACT = 'C', _('Contacto')


class DrugLegality(models.TextChoices):
    LEGAL = 'L', _('De venta legal')
    PRESCIPTION = 'P', _('Solo por prescripción')
    ILLEGAL_C = 'C', _('Ilegal tipo C')
    ILLEGAL_B = 'B', _('Ilegal tipo B')
    ILLEGAL_A = 'A', _('Ilegal tipo A')
    EXPERIMENTAL = 'E', _('Experimental')


class DrugAddiction(models.TextChoices):
    PHYSIOLOGICAL = 'PH', _('Fisiológica')
    PSYCHOLOGICAL = 'PS', _('Sicológica')


class DrugEffect(models.Model):
    name = models.CharField(max_length=200)
    difficult = models.IntegerField()
    decription = models.CharField(max_length=255, null=True, blank=True)
    overdose_decription = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class DrugSideEffect(models.Model):
    name = models.CharField(max_length=200)
    diff_modifier = models.IntegerField()
    decription = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Drug(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    type = models.CharField(max_length=3, choices=DrugType.choices, default=DrugType.DRUG)
    form = models.CharField(max_length=3, choices=DrugForm.choices, default=DrugForm.PILL)
    legality = models.CharField(max_length=3, choices=DrugLegality.choices, default=DrugLegality.LEGAL)
    strength = models.IntegerField()
    dosis = models.CharField(max_length=20)
    presentation = models.CharField(max_length=50)
    speed = models.CharField(max_length=20)
    effects = models.ManyToManyField(to="DrugEffect")
    effects_description = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=20)
    side_effects = models.ManyToManyField(to="DrugSideEffect")
    side_effects_description = models.CharField(max_length=255, null=True, blank=True)
    overdose_description = models.CharField(max_length=255, null=True, blank=True)
    addiction = models.CharField(max_length=3, choices=DrugAddiction.choices, default=DrugAddiction.PHYSIOLOGICAL)
    next_dose = models.CharField(max_length=50)
    symptoms = models.CharField(max_length=50)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class DrugAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "type", "legality", "strength", "cost"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.DRUGS)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Medical Health Care
class MedicalType(models.TextChoices): 
    DOCTOR = 'DOC', _('Visita a Médico')
    CLINIC = 'CLI', _('Visita a Centro Médico')
    HOSPITAL = 'HOS', _('Visita a Hospital')
    INTERN = 'INT', _('Hospitalización')
    SURGERY = 'SUR', _('Cirugía')
    TERAPHY = 'TER', _('Terapia')
    MEDICINE = 'MED', _('Uso de Medicina')


class MedicalQuality(models.TextChoices):
    LOWEST = 'VL', _('Muy Baja')
    LOW = 'L', _('Baja')
    NORMAL = 'N', _('Normal')
    HIGH = 'H', _('Alta')
    HIGHEST = 'VH', _('Muy Alta')
    
    
class Medical(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=3, choices=MedicalType.choices, default=MedicalType.DOCTOR)
    quality = models.CharField(max_length=3, choices=MedicalQuality.choices, default=MedicalQuality.NORMAL)
    elapsed_time = models.IntegerField()
    elapsed_time_uom = models.CharField(max_length=3, choices=TimeUOM.choices, default=TimeUOM.HOURS)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
    
    
class MedicalAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "quality", "cost"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Vehicles
class VehicleType(models.TextChoices): 
    LAND = 'L', _('Vehículos Terrestres')
    AERIAL = 'A', _('Vehículos Aéreos')
    WATER = 'W', _('Vehículos Acuáticos')
    SPACE = 'S', _('Vehículos Espaciales')
  
    
class Vehicle(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=VehicleType.choices, default=VehicleType.LAND)
    top_speed = models.IntegerField(default=0)
    acceleration = models.IntegerField(default=0)
    deceleration = models.IntegerField(default=0)
    crew = models.IntegerField(default=1)
    passengers = models.IntegerField(default=0)
    range = models.IntegerField(default=0)
    cargo = models.IntegerField(default=0)
    maneuverability = models.IntegerField(default=0)
    sp = models.IntegerField(default=0)
    sdp = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    cost = models.BigIntegerField(default=0)
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name


class VehicleAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "brand", "type", "cost"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.ARMOR)
        if db_field.name == "brand":
            kwargs["queryset"] = Brand.objects.filter(type=ItemType.ARMOR)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
