from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability, Surgery

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
        if db_field.name == "surgery":
            kwargs["queryset"] = Surgery.objects.filter()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
