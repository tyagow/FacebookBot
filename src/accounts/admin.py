from django.contrib import admin

# Register your models here.
from src.accounts.models import Profile, Session

admin.site.register(Profile)
admin.site.register(Session)
