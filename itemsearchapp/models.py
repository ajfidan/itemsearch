from django.db import models
from django import forms

class Item(models.Model):
    name = models.TextField()
    price = models.TextField()

#class 