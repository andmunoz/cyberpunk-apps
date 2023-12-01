from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=5, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + " (" + self.code + ")"
    
    
class Brand(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Availability(models.TextChoices): 
    EXCELLENT = 'E', _('Excelente')
    COMMON = 'C', _('Común')
    POOR = 'P', _('Mala')
    RARE = 'R', _('Rara')
    ARMY = 'A', _('Solo Militares')
    EXPERIMENTAL = 'X', _('Experimental')
   

class Concealment(models.TextChoices): 
    POCKET = 'P', _('Bolsillo')
    JACKET = 'J', _('Chaqueta')
    LONG = 'L', _('Chaqueta Larga')
    NONE = 'N', _('No')
   

class Reliability(models.TextChoices): 
    VERY = 'VR', _('Muy Fiable')
    STANDARD = 'ST', _('Fiable')
    UNREL = 'UR', _('Poco Fiable')
   
    
class Weapon(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    availability = models.CharField(max_length=1, choices=Availability.choices, default=Availability.COMMON)
    accuracy = models.IntegerField()
    concealment = models.CharField(max_length=2, choices=Concealment.choices, default=Concealment.JACKET)
    reliability = models.CharField(max_length=2, choices=Reliability.choices, default=Reliability.STANDARD)
    shots = models.IntegerField(blank=True, null=True)
    rof = models.IntegerField(blank=True, null=True)
    range = models.IntegerField(blank=True, null=True)
    damage = models.CharField(max_length=20)
    weight = models.FloatField()
    cost = models.IntegerField()
    image = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.name