# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-26 23:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Quantidade')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120, verbose_name='Produto')),
                ('valor', models.CharField(max_length=80, verbose_name='Valor')),
                ('active', models.BooleanField(default=True, verbose_name='Ativa')),
            ],
        ),
        migrations.AddField(
            model_name='productorder',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='produtos.Produto'),
        ),
        migrations.AddField(
            model_name='productorder',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='bot.Session'),
        ),
    ]
