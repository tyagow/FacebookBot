import datetime
from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase

from src.bot.models import Session, ClientStateEnum
from src.pedidos.models import Pedido


def assertContents(self, contents):
    for expected_content in contents:
        with self.subTest():
            self.assertContains(self.response, expected_content)


class SessionModelTest(TestCase):
    """

    """
    def setUp(self):
        self.user = User.objects.create_user(username='tiago', password='teste123')
        created, self.session = self.user.profile.update_or_create_session()
        self.user.profile.first_name = 'tiago'
        self.user.profile.save()

    def test_create(self):
        self.assertTrue(Session.objects.exists())

    def test_is_expired(self):
        expired_date = self.session.last_active - datetime.timedelta(minutes=20)
        self.session.last_active = expired_date
        self.assertTrue(self.session.is_expired())

    def test_is_valid_expire_old_session(self):
        expired_date = self.session.last_active - datetime.timedelta(minutes=20)
        self.session.last_active = expired_date
        self.session.is_valid()
        self.assertFalse(self.session.active)

    def test_last_update_return_timezone_correct_ctime(self):
        self.assertEqual(self.session.last_updated, self.session.last_active.astimezone().ctime())
    # def test_session(self):

    def test_str(self):
        expected = '{} @ {}'.format(self.session.profile.first_name, self.session.last_updated)
        self.assertEqual(expected, str(self.session))

    @skip
    def test_get_absolute_url(self):
        url = resolve_url('session:detail', slug=self.session.slug)
        self.assertEqual(url, self.session.get_absolute_url())

    def test_initial_state(self):
        self.assertEqual(self.session.state, ClientStateEnum.ENVIAR_MENU)

    def test_cant_create_order_without_valid_address(self):
        pass

    def test_session_can_create_pedido(self):
        self.session.create_pedido()
        self.assertEqual(Pedido.objects.count(), 1)

    # def test_session_create_pedido_set_endereco_default_from_profile(self):
    #     self.assertEself.session.pedidos.first()
