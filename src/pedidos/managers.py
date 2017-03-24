import datetime

from django.db import models


class PedidoModelQuerySet(models.QuerySet):
    def by_user(self, user):
        return self.filter(session__profile__user=user)

    def actives(self, user):
        return self.filter(session__profile__user=user).filter(status=2)

    def realizados(self):
        return self.filter(status__gte=2)

    def hoje(self):
        return self.filter(horario__date=datetime.datetime.today())


PedidoModelManager = models.Manager.from_queryset(PedidoModelQuerySet)
