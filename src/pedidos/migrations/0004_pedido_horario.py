# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 02:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_pedido_entrega'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='horario',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Horario'),
            preserve_default=False,
        ),
    ]
