import datetime

from django.db import models


class PedidoModelManager(models.Manager):
    def by_user(self, user):
        return super(PedidoModelManager, self).filter(session__profile__user=user)

    def actives(self, user):
        return super(PedidoModelManager, self).filter(session__profile__user=user).filter(status=2)

    def realizados(self):
        return super(PedidoModelManager, self).filter(status=2).order_by('horario')

    def hoje(self):
        return super(PedidoModelManager, self).filter(horario__date=datetime.datetime.today()).filter(status__gte=1).order_by('horario')

