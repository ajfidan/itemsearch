from django.db import models
from django import forms

class Item(models.Model):
    name = models.TextField()
    price = models.TextField()

class AllEntity(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "itemsearchapp_item"