from unittest import skip

from django.shortcuts import resolve_url as r
from django.test import TestCase

@skip
class BotViewTest(TestCase):
    def setUp(self):
        fake_message = {
            'data': [{
                'entry': [
                    {
                        'messaging': {
                            'message': {
                                'text': 'Texto Mensagem'
                            },
                            'sender': {
                                'id': 123,
                            },
                        }
                    }
                ]
            }]
        }
        import json
        data = json.dumps(str(fake_message))
        print(data)
        self.response = self.client.post(r('bot:main'), fake_message)

    def test_get(self):
        self.assertEqual(200, self.response.status_code)
