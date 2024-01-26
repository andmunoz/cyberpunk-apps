from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability, TimeUOM


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