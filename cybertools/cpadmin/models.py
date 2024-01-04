from django.db import models
from django.utils.translation import gettext_lazy as _


### General Models
class ItemType(models.TextChoices):
    WEAPON = 'WEAPON', _('Armas')
    ARMOR = 'ARMOR', _('Blindaje')
    GEAR = 'GEAR', _('Equipo')
    CYBER = 'CYBER', _('Ciberequipo')
    CLOTHES = 'CLOTHES', _('Moda')
    MEDICAL = 'MEDICAL', _('Medicina')
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
        return "[" + ItemType(self.type).label + "] " + self.name + " (" + self.code + ")"
    
    
class Brand(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.WEAPON)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return "[" + ItemType(self.type).label + "] " + self.name


class Availability(models.TextChoices): 
    EXCELLENT = 'E', _('Excelente')
    COMMON = 'C', _('Común')
    POOR = 'P', _('Mala')
    RARE = 'R', _('Rara')
    ARMY = 'A', _('Solo Militares')
    EXPERIMENTAL = 'X', _('Experimental')
   

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
    weight = models.FloatField()
    cost = models.IntegerField()
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name
    
    
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
    weight = models.FloatField()
    cost = models.IntegerField()
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name


### Specific Models for Gear
class GearType(models.TextChoices): 
    OPTIONAL = 'OPT', _('Opcional')


class Gear(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    type = models.CharField(max_length=3, choices=GearType.choices, default=GearType.OPTIONAL)
    weight = models.FloatField()
    cost = models.IntegerField()
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


### Specific Models for Cyberware
class CyberType(models.TextChoices): 
    IMPLANT = 'IMP', _('Implante')
    MODULE = 'MOD', _('Módulo')
    MRAM = 'MRAM', _('Chip de Memoria')
    CPART = 'CPART', _('Chip de Reflejos')


class SurgeryTypes(models.TextChoices): 
    NO = 'NO', _('No Aplica')
    INSIGNIFICANT = 'IN', _('Insignificante')
    SECONDARY = 'SE', _('Secundaria')
    IMPORTANT = 'IM', _('Importante')
    CRITICAL = 'CR', _('Crítica')


class CyberSurgery(models.Model):
    type = models.CharField(max_length=2, choices=SurgeryTypes.choices)
    difficulty = models.IntegerField()
    time_length = models.IntegerField()
    damage = models.CharField(max_length=10, default='No')
    cost = models.IntegerField()

    def __str__(self):
        return SurgeryTypes(self.type).label
    

class Cyberware(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    type = models.CharField(max_length=3, choices=GearType.choices, default=GearType.OPTIONAL)
    humanity = models.CharField(max_length=10, null=True)
    requirement = models.ForeignKey("Cyberware", on_delete=models.CASCADE, null=True, blank=True)
    adjustment = models.CharField(max_length=100, null=True)
    slot = models.CharField(max_length=100, null=True)
    surgery = models.ForeignKey("CyberSurgery", on_delete=models.CASCADE)
    weight = models.FloatField()
    cost = models.IntegerField()
    description = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
