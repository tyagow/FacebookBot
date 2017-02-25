from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.shortcuts import resolve_url
from django.test import TestCase

from src.core.models import Empresa


def assertContents(self, contents):
    for expected_content in contents:
        with self.subTest():
            self.assertContains(self.response, expected_content)


class ProfileModelTest(TestCase):
    """

    """
    def setUp(self):
        self.profile = Profile.objects.create(nome='Vivo', slug='vivo', logo='logo.png')

    def test_create(self):
        self.assertTrue(Empresa.objects.exists())

    def test_str(self):
        self.assertEqual(self.profile.nome, str(self.profile))

    def test_get_absolute_url(self):
        url = resolve_url('accounts:detail', slug=self.profile.slug)
        self.assertEqual(url, self.profile.get_absolute_url())

