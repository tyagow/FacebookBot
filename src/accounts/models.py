from __future__ import unicode_literals

from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    fbid = models.CharField(blank=True, max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    slug = models.SlugField(null=True, unique=True)
    picture = models.URLField(blank=True)
    first_name = models.CharField(blank=True, max_length=40)
    last_name = models.CharField(blank=True, max_length=40)
    timezone = models.IntegerField(blank=True)
    gender = models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)
    telefone = models.CharField(blank=True, max_length=20)
