from unittest import skip

import mock as mock
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase

from src.bot.models import Session
from src.produtos.models import Produto, ProductOrder


def assertContents(self, contents):
    for expected_content in contents:
        with self.subTest():
            self.assertContains(self.response, expected_content)


class ProdutoManagerTest(TestCase):
    """

    """

    def setUp(self):
        self.produto = Produto.objects.create(nome='Frango', valor=25.00)
        Produto.objects.create(nome='Frango', valor=25.00, active=False)

    def test_filter_by_active(self):
        produtos_ativos = Produto.objects.ativos()
        self.assertEqual(produtos_ativos.count(), 1)


class ProdutoModelTest(TestCase):
    """

    """
    def setUp(self):
        self.produto = Produto.objects.create(nome='Frango', valor=25.00)

    def test_create(self):
        self.assertTrue(Produto.objects.exists())

    def test_str(self):
        self.assertEqual(self.produto.nome, str(self.produto))

    def test_active_default_true(self):
        self.assertTrue(self.produto.active)

    @skip
    def test_get_absolute_url(self):
        url = resolve_url('produtos:detail', slug=self.produto.slug)
        self.assertEqual(url, self.produto.get_absolute_url())


class ProductOrderModelTest(TestCase):
    """

    """
    def setUp(self):
        self.user = User.objects.create_user(username='tiago', password='teste123')
        created, self.session = self.user.profile.update_or_create_session()

        self.produto = Produto.objects.create(nome='Frango', valor=25.00)
        self.pedido = self.session.create_pedido()

        self.product_order = ProductOrder.objects.create(produto=self.produto, amount=1, pedido=self.pedido)

    def test_create(self):
        self.assertTrue(ProductOrder.objects.exists())

    def test_str(self):
        expected = '{} {} - R${}'.format(self.product_order.amount, self.product_order.nome, self.product_order.valor_total)
        self.assertEqual(expected, str(self.product_order))
