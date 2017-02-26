import datetime
from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.test import TestCase

from src.accounts.models import Session


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

    def test_update_or_create_should_expired_old_active_session(self):
        expired_date = self.session.last_active - datetime.timedelta(minutes=20)
        self.session.last_active = expired_date
        created, self.session = self.user.profile.update_or_create_session()
        self.assertEqual(Session.objects.count(), 2)
        self.assertTrue(created)

    def test_last_update_return_timezone_correct_ctime(self):
        self.assertEqual(self.session.last_updated, self.session.last_active.astimezone().ctime())
    # def test_session(self):


    @skip
    def test_str(self):
        self.assertEqual(self.session.user.username, str(self.session))

    @skip
    def test_slug_auto_create(self):
        self.assertEqual(self.session.slug, 'tiago')

    @skip
    def test_get_absolute_url(self):
        url = resolve_url('session:detail', slug=self.session.slug)
        self.assertEqual(url, self.session.get_absolute_url())

