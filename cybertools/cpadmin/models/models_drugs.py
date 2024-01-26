from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ItemType, Category, Brand, Availability


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
