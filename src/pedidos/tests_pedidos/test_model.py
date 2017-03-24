import datetime
from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase

from src.pedidos.models import Pedido
from src.pedidos.utils import time_valid, isDateTimeFormat, isTimeFormat
from src.produtos.models import Produto


def assertContents(self, contents):
    for expected_content in contents:
        with self.subTest():
            self.assertContains(self.response, expected_content)


class PedidoModelManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tiago', password='teste123')
        self.userB = User.objects.create_user(username='tiagoB', password='teste123')
        created, self.sessionB = self.userB.profile.update_or_create_session()
        self.pedidoB = self.sessionB.create_pedido()
        self.pedidoB.active = False
        self.pedidoB.save()

        created, self.session = self.user.profile.update_or_create_session()
        self.pedido = self.session.create_pedido()

    def test_filter_by_user(self):
        self.assertEqual(self.pedido, Pedido.objects.by_user(self.user)[0])
        self.assertEqual(1, Pedido.objects.by_user(self.user).count())

    def test_filter_active_only(self):
        """PedidoManager deve ter um metodo que retorne somente os pedidos ativos"""
        self.pedido.status = 2
        self.pedido.save()
        self.assertEqual(self.pedido, Pedido.objects.actives(self.user)[0])

        self.assertEqual(1, Pedido.objects.actives(self.user).count())

    def test_realizados(self):
        """PedidoManager deve ter um metodo que retorne somente os pedidos realizados"""
        self.pedido.status = 2
        self.pedido.save()
        self.assertEqual(self.pedido, Pedido.objects.realizados()[0])

    def test_hoje(self):
        """Pedidos.objects.hoje deve retornar pedidos que sejam para hoje"""
        hoje = datetime.datetime.strptime('23/3/2017 00:01', '%d/%m/%Y %H:%M')
        self.pedido.set_horario('23/3/2017 10:30')
        self.pedidoB.set_horario('22/3/2017 10:30')
        self.pedido.save()
        self.pedidoB.save()
        self.assertEqual(self.pedido, Pedido.objects.hoje()[0])


class PedidoModelTest(TestCase):
    """
    Pedido deve conter:
        - Uma sessao
        - Lista de produtos
        - Endereço
        - Observação
        - Slug
        - Valor Total
        - Timestamp
        - last_updated
        - Status:
                - Aberto
                - Realizado
                - Enviado
                - Finalizado
    """
    def setUp(self):
        self.user = User.objects.create_user(username='tiago', password='teste123')
        created, self.session = self.user.profile.update_or_create_session()
        self.pedido = self.session.create_pedido()

    def test_create(self):
        self.assertTrue(Pedido.objects.exists())

    def test_has_endereco_on_create(self):
        field = Pedido._meta.get_field('endereco')
        self.assertFalse(field.blank)

    def test_observacao_can_be_blank(self):
        field = Pedido._meta.get_field('observacao')
        self.assertTrue(field.blank)

    @skip
    def test_slug_auto_create(self):
        self.assertEqual(self.pedido.slug, 'tiago')

    def test_status_choices_display(self):
        """
         Status:
               1 - Aberto
               2 - Realizado
               3 - Enviado
               4 - Finalizado
        """
        self.pedido.status = 1
        self.assertEqual(self.pedido.get_status_display(), 'Aberto')
        self.pedido.status = 2
        self.assertEqual(self.pedido.get_status_display(), 'Realizado')
        self.pedido.status = 3
        self.assertEqual(self.pedido.get_status_display(), 'Enviado')
        self.pedido.status = 4
        self.assertEqual(self.pedido.get_status_display(), 'Finalizado')

    def test_cidade_choices_validation(self):
        """status should be limited to 1, 2, 3 or 4"""
        self.pedido.status = 'TESTE'
        self.assertRaises(ValidationError, self.pedido.full_clean)

    def test_pedido_valor_total(self):
        self.assertEqual(self.pedido.valor_total, 0)

    def test_pedido_tipo_entrega_choices_display(self):
        """
         tipo_entrega:
               1 - MotoBoy
               2 - Retirar no local
        """
        self.pedido.entrega = 1
        self.assertEqual(self.pedido.get_entrega_display(), 'MotoBoy')
        self.pedido.entrega = 2
        self.assertEqual(self.pedido.get_entrega_display(), 'Retirar no local')

    def test_time_validation(self):
        self.assertTrue(isTimeFormat('10:20'))
        self.assertTrue(isDateTimeFormat('12/3/17 10:20'))
        self.assertTrue(isDateTimeFormat('12/3/2017 10:20'))

    def test_horario_field(self):
        field = self.pedido._meta.get_field('horario')
        self.assertTrue(field.blank)

    def test_horario_hora(self):
        self.pedido.set_horario('10/3/2017 10:30')
        self.assertEqual(self.pedido.horario_hora, '10:30')

    def test_get_absolute_url(self):
        url = resolve_url('pedido:detail', pk=self.pedido.pk)
        self.assertEqual(url, self.pedido.get_absolute_url())
