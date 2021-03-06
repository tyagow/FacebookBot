# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-26 20:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0005_auto_20170321_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='origin',
            field=models.IntegerField(choices=[(1, 'Facebook'), (2, 'Loja')], default=1, verbose_name='Origem Pedido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='bot.Session'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(1, 'Aberto'), (20, 'Lista de Produtos'), (50, 'Selecionando Produto'), (55, 'Adicionando Mais Produtos'), (60, 'Quantidade do produto'), (70, 'Tipo de Entrega'), (75, 'Horario'), (80, 'Endereco para entrega'), (100, 'Observação'), (120, 'Confirmando pedido'), (200, 'Pedido Feito')], default=1),
        ),
    ]
