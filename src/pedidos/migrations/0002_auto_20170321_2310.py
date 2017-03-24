# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 02:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.IntegerField(choices=[(1, 'Aberto'), (2, 'Realizado'), (3, 'Enviado'), (4, 'Finalizado'), (5, 'Abandonado')], default=1, verbose_name='Status'),
        ),
    ]