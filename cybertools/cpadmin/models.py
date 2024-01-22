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
    name = models.CharField(max_length=200, verbose_name="Nombre")
    code = models.CharField(max_length=5, blank=True, verbose_name="Código")
    type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.WEAPON, verbose_name="Tipo")
    description = models.CharField(max_length=1000, blank=True, verbose_name="descripción")
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True, verbose_name="padre")

    def __str__(self):
        return self.name


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "type", "parent"]
    
    
class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.WEAPON, verbose_name="Tipo")
    description = models.CharField(max_length=1000, blank=True, verbose_name="descripción")

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
class Weapon(models.Model):
    class Concealment(models.TextChoices): 
        POCKET = 'P', _('Bolsillo')
        JACKET = 'J', _('Chaqueta')
        LONG = 'L', _('Chaqueta Larga')
        NONE = 'N', _('No')
   
    class Reliability(models.TextChoices): 
        VERY = 'VR', _('Muy Fiable')
        STANDARD = 'ST', _('Fiable')
        UNREL = 'UR', _('Poco Fiable')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON, verbose_name="Disponibilidad")
    accuracy = models.IntegerField(verbose_name="Precisión")
    concealment = models.CharField(max_length=2, choices=Concealment.choices, default=Concealment.JACKET, verbose_name="Disimulo")
    reliability = models.CharField(max_length=2, choices=Reliability.choices, default=Reliability.STANDARD, verbose_name="Fiabilidad")
    shots = models.IntegerField(blank=True, null=True, verbose_name="Disparos")
    rof = models.IntegerField(blank=True, null=True, verbose_name="Disparos por Ronda")
    range = models.IntegerField(blank=True, null=True, verbose_name="Alcance")
    damage = models.CharField(max_length=20, verbose_name="Daño")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")
    
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
class Armor(models.Model):
    class Type(models.TextChoices): 
        SOFT = 'S', _('Blando')
        HARD = 'H', _('Duro')   
    
    class Coverage(models.TextChoices): 
        HEAD = 'HEAD', _('Cabeza')
        TORSO = 'TORSO', _('Torso')
        UPPER = 'UPPER', _('Torso y Brazos')
        LOWER = 'LOWER', _('Piernas')
        BODY = 'BODY', _('Cuerpo')
        FULL = 'FULL', _('Todo')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON, verbose_name="Disponibilidad")
    coverage = models.CharField(max_length=20, choices=Coverage.choices, default=Coverage.BODY, verbose_name="Cobertura")
    type = models.CharField(max_length=1, choices=Type.choices, default=Type.HARD, verbose_name="Tipo")
    sp = models.IntegerField(verbose_name="CP")
    ev = models.IntegerField(verbose_name="CE")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")
    
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
class Gear(models.Model):
    class Type(models.TextChoices): 
        OPTIONAL = 'OPT', _('Opcional')
    
    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON, verbose_name="Disponibilidad")
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.OPTIONAL, verbose_name="Tipo")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")

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
class Surgery(models.Model):
    class Type(models.TextChoices): 
        NO = 'NO', _('No Aplica')
        INSIGNIFICANT = 'IN', _('Insignificante')
        SECONDARY = 'SE', _('Secundaria')
        IMPORTANT = 'IM', _('Importante')
        CRITICAL = 'CR', _('Crítica')
    
    type = models.CharField(max_length=2, choices=Type.choices, verbose_name="Tipo")
    difficulty = models.IntegerField(verbose_name="Dificultad")
    time_length = models.IntegerField(verbose_name="Duración")
    damage = models.CharField(max_length=10, default='No', verbose_name="Daño")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")

    def __str__(self):
        return self.get_type_display()


class SurgeryAdmin(admin.ModelAdmin):
    list_display = ["type", "difficulty", "time_length", "damage", "cost"]
    

### Specific Models for Cyberware
class Cyberware(models.Model):
    class Type(models.TextChoices): 
        IMPLANT = 'IMP', _('Implante')
        EXTERNAL = 'EXT', _('Externo')
        ADDON = 'ADD', _('Opción')
        IMPROVEMENT = 'IMPRO', _('Mejora')
        MRAM = 'MRAM', _('Chip de Memoria')
        CPART = 'CPART', _('Chip de Reflejos')


    class Slot(models.TextChoices):
        FULL = 'FUL', _('Cuerpo y Cabeza')
        HEAD = 'HEA', _('Cabeza')
        BODY = 'BOD', _('Cuerpo')
        TORSO = 'TOR', _('Torso')
        ARM = 'ARM', _('Brazo')
        ARMLEG = 'AOL', _('Brazo o Pierna')
        LEG = 'LEG', _('Pierna')
        CROTCH = 'CRO', _('Ingle')
    
    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON, verbose_name="Disponibilidad")
    type = models.CharField(max_length=5, choices=Type.choices, default=Type.IMPLANT, verbose_name="Tipo")
    humanity = models.CharField(max_length=10, null=True, verbose_name="Costo Humanidad")
    requirement = models.CharField(max_length=100, null=True, blank=True, verbose_name="Requisito")
    adjustment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Ajustes")
    slot = models.CharField(max_length=3, choices=Slot.choices, default=Slot.FULL, verbose_name="Localización")
    surgery = models.ForeignKey("Surgery", on_delete=models.CASCADE, verbose_name="Tipo de Cirugía")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")

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
class Clothes(models.Model):
    class Type(models.TextChoices): 
        UNISEX = 'U', _('Unisex')
        MALE = 'M', _('Masculino')
        FEMALE = 'F', _('Femenino')
        NO = 'N', _('Sin Tipo')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON, verbose_name="Disponibilidad")
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.NO, verbose_name="Tipo")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")

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
class DrugEffect(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    difficult = models.IntegerField(verbose_name="Dificultad")
    decription = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción")
    overdose_decription = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sobredosis")

    def __str__(self):
        return self.name


class DrugEffectAdmin(admin.ModelAdmin):
    list_display = ["name", "difficult"]


class DrugSideEffect(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    diff_modifier = models.IntegerField(verbose_name="Modificador")
    decription = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.name


class DrugSideEffectAdmin(admin.ModelAdmin):
    list_display = ["name", "diff_modifier"]


class Drug(models.Model):
    class Type(models.TextChoices): 
        BEVERAGE = 'B', _('Bebidas Alcohólicas')
        CIGARRETTE = 'C', _('Cigarrillos')
        MEDICINE = 'M', _('Fármaco')
        DRUG = 'D', _('Droga')

    class Form(models.TextChoices):
        PILL = 'P', _('Píldora o Tableta')
        GELCAP = 'G', _('Cápsula')
        PAPER = 'T', _('Pestaña de Papel')
        SMOKE = 'S', _('Fumado, Inhalado')
        POWDER = 'PI', _('En polvo, Inhalado')
        INJECTED = 'I', _('Inyectado')
        LIQUID = 'L', _('Líquido')
        BAND = 'B', _('Parche')
        CONTACT = 'C', _('Contacto')

    class Legality(models.TextChoices):
        LEGAL = 'L', _('De venta legal')
        PRESCIPTION = 'P', _('Solo por prescripción')
        ILLEGAL_C = 'C', _('Ilegal tipo C')
        ILLEGAL_B = 'B', _('Ilegal tipo B')
        ILLEGAL_A = 'A', _('Ilegal tipo A')
        EXPERIMENTAL = 'E', _('Experimental')

    class Addiction(models.TextChoices):
        PHYSIOLOGICAL = 'PH', _('Fisiológica')
        PSYCHOLOGICAL = 'PS', _('Sicológica')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.DRUG, verbose_name="Tipo")
    form = models.CharField(max_length=3, choices=Form.choices, default=Form.PILL, verbose_name="Forma")
    legality = models.CharField(max_length=3, choices=Legality.choices, default=Legality.LEGAL, verbose_name="Legalidad")
    strength = models.IntegerField(verbose_name="Fuerza")
    dosis = models.CharField(max_length=20, verbose_name="Dosis")
    presentation = models.CharField(max_length=50, verbose_name="Presentación")
    speed = models.CharField(max_length=20, verbose_name="Velocidad de Efecto")
    effects = models.ManyToManyField(to="DrugEffect", verbose_name="Efectos")
    effects_description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción Efectos")
    duration = models.CharField(max_length=20, verbose_name="Duración Efectos")
    side_effects = models.ManyToManyField(to="DrugSideEffect", verbose_name="Efectos Secundarios")
    side_effects_description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Descripción de Efectos Secundarios")
    overdose_description = models.CharField(max_length=255, null=True, blank=True, verbose_name="Sobredosis")
    addiction = models.CharField(max_length=3, choices=Addiction.choices, default=Addiction.PHYSIOLOGICAL, verbose_name="Tipo de Adicción")
    next_dose = models.CharField(max_length=50, verbose_name="Tiempo Siguiente Dosis")
    symptoms = models.CharField(max_length=50, verbose_name="Tiempo Síntomas")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.name


class DrugAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "type", "legality", "strength", "cost"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(type=ItemType.DRUGS)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Medical Health Care
class Medical(models.Model):
    class Type(models.TextChoices): 
        DOCTOR = 'DOC', _('Visita a Médico')
        CLINIC = 'CLI', _('Visita a Centro Médico')
        HOSPITAL = 'HOS', _('Visita a Hospital')
        INTERN = 'INT', _('Hospitalización')
        SURGERY = 'SUR', _('Cirugía')
        TERAPHY = 'TER', _('Terapia')
        MEDICINE = 'MED', _('Uso de Medicina')

    class Quality(models.TextChoices):
        LOWEST = 'VL', _('Muy Baja')
        LOW = 'L', _('Baja')
        NORMAL = 'N', _('Normal')
        HIGH = 'H', _('Alta')
        HIGHEST = 'VH', _('Muy Alta')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    type = models.CharField(max_length=3, choices=Type.choices, default=Type.DOCTOR, verbose_name="Tipo")
    quality = models.CharField(max_length=3, choices=Quality.choices, default=Quality.NORMAL, verbose_name="Calidad")
    elapsed_time = models.IntegerField(verbose_name="Tiempo")
    elapsed_time_uom = models.CharField(max_length=3, choices=TimeUOM.choices, default=TimeUOM.HOURS, verbose_name="Unidad")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.name
    
    
class MedicalAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "quality", "cost"]
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


### Specific Models for Vehicles
class Vehicle(models.Model):
    class Type(models.TextChoices): 
        LAND = 'L', _('Vehículos Terrestres')
        AERIAL = 'A', _('Vehículos Aéreos')
        WATER = 'W', _('Vehículos Acuáticos')
        SPACE = 'S', _('Vehículos Espaciales')

    name = models.CharField(max_length=200, verbose_name="Nombre")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Categoría")
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marca")
    type = models.CharField(max_length=1, choices=Type.choices, default=Type.LAND, verbose_name="Tipo")
    top_speed = models.IntegerField(default=0, verbose_name="Velocidad Máxima")
    acceleration = models.IntegerField(default=0, verbose_name="Aceleración")
    deceleration = models.IntegerField(default=0, verbose_name="Desaceleración")
    crew = models.IntegerField(default=1, verbose_name="Tripulación")
    passengers = models.IntegerField(default=0, verbose_name="Pasajeros")
    autonomy = models.IntegerField(default=0, verbose_name="Autonomía")
    cargo = models.IntegerField(default=0, verbose_name="Carga")
    maneuverability = models.IntegerField(default=0, verbose_name="Maniobrabilidad")
    sp = models.IntegerField(default=0, verbose_name="CP")
    sdp = models.IntegerField(default=0, verbose_name="PDE")
    weight = models.FloatField(default=0, verbose_name="Peso")
    cost = models.BigIntegerField(default=0, verbose_name="Precio")
    description = models.CharField(max_length=255, null=True, verbose_name="Descripción")
    image = models.CharField(max_length=255, null=True, verbose_name="Imagen")
    
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
