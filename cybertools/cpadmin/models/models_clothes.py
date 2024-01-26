from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability


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
