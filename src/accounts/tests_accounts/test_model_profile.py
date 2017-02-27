from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase

from src.accounts.models import Profile
from src.bot.models import Session


def assertContents(self, contents):
    for expected_content in contents:
        with self.subTest():
            self.assertContains(self.response, expected_content)


class ProfileModelTest(TestCase):
    """
    Profile deve conter informações coletadas do facebook:
      - facebook id
      - first_name
      - last_name
      - picture url
      - gender
      - timezone
    Profile deve ter um metodo que carrega os detalhes do facebook
    """
    def setUp(self):
        self.user = User.objects.create_user(username='tiago', password='teste123')
        self.profile = self.user.profile

    def test_create(self):
        self.assertTrue(Profile.objects.exists())

    def test_str(self):
        self.assertEqual(self.profile.user.username, str(self.profile))

    def test_slug_auto_create(self):
        self.assertEqual(self.profile.slug, 'tiago')

    def test_cidade_choices_display(self):
        """
        gender deve ser limitado a 'M' ou 'F'
        gender display deve mostrar Masculino para M e Feminino para F
        """
        self.profile.gender = 'M'
        self.assertEqual(self.profile.get_gender_display(), 'Masculino')
        self.profile.gender = 'F'
        self.assertEqual(self.profile.get_gender_display(), 'Feminino')

    def test_cidade_choices_validation(self):
        """gender should be limited to F or M"""
        self.profile.gender = 'TESTE'
        self.assertRaises(ValidationError, self.profile.full_clean)

    def test_user_details_load(self):
        user_details = {
            "first_name": "Tiago",
            "last_name": "Almeida",
            "profile_pic": "https://scontent.xx.fbcdn.net/v/t31.0-1/14681116_1304051606292232_6386653721676889855_o.jpg?oh=7ddac19a566d87bd7d864efb2c9561dd&oe=592750DE",
            "locale": "pt_BR",
            "timezone": -3,
            "gender": "male"
        }
        self.profile.save_details('1231234512351', user_details)
        self.assertEqual(self.profile.first_name, 'Tiago')
        self.assertEqual(self.profile.last_name, 'Almeida')
        self.assertEqual(self.profile.picture, 'https://scontent.xx.fbcdn.net/v/t31.0-1/14681116_1304051606292232_6386653721676889855_o.jpg?oh=7ddac19a566d87bd7d864efb2c9561dd&oe=592750DE')
        self.assertEqual(self.profile.timezone, -3)
        self.assertEqual(self.profile.gender, 'M')

    # @skip
    def test_has_sessions(self):
        created, session = self.profile.update_or_create_session()
        self.assertEqual(self.profile.sessions.count(), 1)
        self.assertTrue(created)

    def test_session_property_has_last_active_session(self):
        created, session = self.profile.update_or_create_session()
        self.assertIsInstance(self.profile.session, Session)

    @skip
    def test_get_absolute_url(self):
        url = resolve_url('accounts:detail', slug=self.profile.slug)
        self.assertEqual(url, self.profile.get_absolute_url())

