from django.db import models

# Create your models here.

class Activity(models.Model):
    name_category_sector_description= models.TextField(max_length=2000)
    region = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    co2e_factor = models.DecimalField(max_digits=10,decimal_places=4)
    co2 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    ch4 = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    n2o = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    class Meta: 
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

class Cart(models.Model):
    co2e = models.DecimalField(max_digits=10, decimal_places = 4)
