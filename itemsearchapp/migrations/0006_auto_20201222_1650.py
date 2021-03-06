# Generated by Django 3.1.3 on 2020-12-22 23:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('itemsearchapp', '0005_item_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='isTracked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
