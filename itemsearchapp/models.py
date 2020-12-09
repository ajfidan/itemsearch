from django.db import models
from django import forms

class Item(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

class AllEntity(models.Model):
    name = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "itemsearchapp_item"