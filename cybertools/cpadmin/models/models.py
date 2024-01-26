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
    
