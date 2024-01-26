from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability


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