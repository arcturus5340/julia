from django.test import Client, TestCase

from auth.models import User

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            username='TestUsername',
            email='TestEmail',
        )
        user.set_password('TestPassword')
        user.save()

    def test_unauthorized_list(self):
        client = Client()
        response = client.get('/api/v1/users/')

        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'username': 'TestUsername',
                    'first_name': '',
                    'last_name': '',
                    'last_login': None
                }
            ]
        }


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
