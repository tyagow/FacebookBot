# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170221_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.URLField(blank=True),
        ),
    ]
