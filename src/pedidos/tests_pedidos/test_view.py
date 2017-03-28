import datetime
from unittest import skip

from django.shortcuts import resolve_url as r
from django.test import RequestFactory
from django.test import TestCase
from model_mommy import mommy

from src.bot.models import Session
from src.pedidos.models import Pedido
from src.pedidos.views import PedidoDetailView
from src.tests_utils.factory import UserFactory, SessionFactory


class PedidoListTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('pedido:list'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)


class PedidoDetailViewTest(TestCase):
    """
    """

    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        session = Session.objects.create(profile=self.user.profile)
        self.pedido = Pedido.objects.create(session=session,horario=datetime.datetime.now())
        self.response = self.client.get(r('pedido:detail', 1))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

@skip
class PedidoUpdateViewTest(TestCase):
    """
    """

    def setUp(self):
        self.user = UserFactory()
        self.user.save()
        session = Session.objects.create(profile=self.user.profile)
        self.pedido = Pedido.objects.create(session=session, horario=datetime.datetime.now())
        self.response = self.client.get(r('pedido:update', self.pedido.pk))

    @skip
    def test_get(self):
        self.assertEqual(200, self.response.status_code)
