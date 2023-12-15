from django.db import models

# Create your models here.

# app1/models.py


class District(models.Model):
    name = models.CharField(max_length=255)

class Taluka(models.Model):
    name = models.CharField(max_length=300)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

class Village(models.Model):
    name = models.CharField(max_length=300)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE)
