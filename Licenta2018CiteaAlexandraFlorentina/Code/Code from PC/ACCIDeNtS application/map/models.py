from django.db import models
from datetime import datetime


class Incident(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(default=datetime.now)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    accidentsPriority = models.IntegerField(default=0)
    resolved = models.BooleanField(default=0)


class Unit(models.Model):
    id = models.IntegerField(primary_key=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    accidents = models.ForeignKey(Incident, on_delete=models.CASCADE, default=0)