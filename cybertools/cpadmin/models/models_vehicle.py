from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand


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
