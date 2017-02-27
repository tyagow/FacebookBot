# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_auto_20170226_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productorder',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='valor',
            field=models.FloatField(max_length=10, verbose_name='Valor'),
        ),
    ]
