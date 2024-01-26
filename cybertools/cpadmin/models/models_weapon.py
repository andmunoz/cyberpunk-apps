from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability


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