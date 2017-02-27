from django.shortcuts import resolve_url as r
from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.response = self.client.get(r('core:home'))

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'core/index.html')