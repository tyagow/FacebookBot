from django.db import models


class SessionManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(SessionManager, self).filter(active=True).order_by('-pk').first()

