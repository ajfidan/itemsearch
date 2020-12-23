from django.db import models
from django import forms
from django.utils.timezone import now

class Item(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    image_url = models.TextField()
    isTracked = models.BooleanField(default=False)
    created = models.DateTimeField(default=now, editable=False)

class AllEntity(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    image_url = models.TextField()
    isTracked = models.BooleanField(default=False)
    created = models.DateTimeField(default=now, editable=False)

    class Meta:
        managed = False
        db_table = "itemsearchapp_item"