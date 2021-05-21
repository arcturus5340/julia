from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group
from django.core.files import File
from django.core import mail
from django.contrib import auth
from django.conf import settings

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from auth.models import Activation

import os


class UserTestCase(APITestCase):
    def setUp(self):
        verified_users_group = Group.objects.create(name='Verified Users')
        self.first_user = auth.get_user_model().objects.create(
            username='TestUsername1',
            email='TestEmail1',
        )
        self.first_user.set_password('TestPassword1')
        self.first_user.text_password = 'TestPassword1'
        self.first_user.groups.add(verified_users_group)
        self.first_user.save()

        self.second_user = auth.get_user_model().objects.create(
            username='TestUsername2',
            email='TestEmail2',
        )
        self.second_user.set_password('TestPassword2')
        self.second_user.text_password = 'TestPassword2'
        self.second_user.groups.add(verified_users_group)
        self.second_user.save()

        self.admin_user = auth.get_user_model().objects.create(
            username='TestAdminUsername',
            email='TestAdminEmail',
            is_staff=True,
        )
        self.admin_user.set_password('TestAdminPassword')
        self.admin_user.text_password = 'TestAdminPassword'
        self.admin_user.groups.add(verified_users_group)

        self.admin_user.save()
        self.full_result_keys = ('id', 'username', 'email', 'date_joined', 'last_login')
        self.basic_result_keys = ('id', 'username', 'date_joined', 'last_login')

    @staticmethod
    def authorize(user, username=None, password=None):
        sign_in_data = {
            'username': username or user.username,
            'password': password or user.text_password,
        }

        client = APIClient()
        response = client.post('/api/token-auth', data=sign_in_data, format='json')
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        return client

    def test_unauthorized_head(self):
        client = APIClient()
        response = client.head('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_head(self):
        client = self.authorize(self.first_user)
        response = client.head('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_head(self):
        client = self.authorize(self.admin_user)
        response = client.head('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_list(self):
        client = APIClient()
        response = client.get('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.basic_result_keys)

    def test_authorized_list(self):
        client = self.authorize(self.first_user)
        response = client.get('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.full_result_keys)

    def test_admin_list(self):
        client = self.authorize(self.first_user)
        response = client.get('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.full_result_keys)

    def test_list_filter(self):
        client = APIClient()
        response = client.get('/api/users/?username=TestUsername1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_search(self):
        client = APIClient()
        response = client.get('/api/users/?search={}'.format(self.first_user.username))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unauthorized_create(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        sign_up_data = {
            'username': 'SignUpTestUsername',
            'password': 'st@ngpa$$wort',
            'email': 'signup@test.email',
            'email_template': upload_file,
        }

        client = APIClient()
        response = client.post(
            '/api/users/',
            data=sign_up_data,
            content_disposition='attachment; filename=email_template.html',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tuple(response.data.keys()), self.basic_result_keys)
        self.assertEqual(auth.get_user_model().objects.count(), 4)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Registration')

        os.remove(f'{settings.EMAIL_TEMPLATES_ROOT}email_template.html')

    def test_authorized_create(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        sign_up_data = {
            'username': 'SignUpTestUsername',
            'password': 'SignUpTestPassword',
            'email': 'signup@test.email',
            'email_template': upload_file,
        }

        client = self.authorize(self.first_user)
        response = client.post(
            '/api/users/',
            data=sign_up_data,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth.get_user_model().objects.count(), 3)
        self.assertEqual(len(mail.outbox), 0)

    def test_admin_create(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        sign_up_data = {
            'username': 'SignUpTestUsername',
            'password': 'SignUpTestPassword',
            'email': 'signup@test.email',
            'email_template': upload_file,
        }

        client = self.authorize(self.admin_user)
        response = client.post(
            '/api/users/',
            data=sign_up_data,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(auth.get_user_model().objects.count(), 3)
        self.assertEqual(len(mail.outbox), 0)

    def test_create_without_template(self):
        sign_up_data = {
            'username': 'SignUpTestUsername',
            'password': 'str0ngpa$$wort',
            'email': 'signup@test.email',
        }

        client = APIClient()
        response = client.post('/api/users/', data=sign_up_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tuple(response.data.keys()), self.basic_result_keys)
        self.assertEqual(auth.get_user_model().objects.count(), 4)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Registration')

    def test_unauthorized_retrieve(self):
        client = APIClient()
        response = client.get('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.basic_result_keys)

    def test_authorized_retrieve(self):
        client = self.authorize(self.second_user)
        response = client.get('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.full_result_keys)

    def test_owner_retrieve(self):
        client = self.authorize(self.first_user)
        response = client.get('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.full_result_keys)

    def test_admin_retrieve(self):
        client = self.authorize(self.admin_user)
        response = client.get('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.full_result_keys)

    def test_non_existent_retrieve(self):
        client = self.authorize(self.admin_user)
        response = client.get('/api/users/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_partial_update(self):
        updates = {
            'username': 'NewUsername1',
        }

        client = APIClient()
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')

    def test_authorized_partial_update(self):
        updates = {
            'username': 'NewUsername2',
        }

        client = self.authorize(self.second_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')

    def test_owner_partial_update(self):
        updates = {
            'username': 'NewUsername1',
        }

        client = self.authorize(self.first_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')
        self.assertEqual(tuple(response.data.keys()), self.full_result_keys)

    def test_admin_partial_update(self):
        updates = {
            'username': 'NewUsername1',
        }

        client = self.authorize(self.admin_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')
        self.assertEqual(tuple(response.data.keys()), self.full_result_keys)

    def test_unauthorized_reset_password(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }
        client = APIClient()
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

        os.remove(f'{settings.EMAIL_TEMPLATES_ROOT}email_template.html')

    def test_authorized_reset_password(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = self.authorize(self.second_user)
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

    def test_owner_reset_password(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = self.authorize(self.first_user)
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

    def test_admin_reset_password(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = self.authorize(self.admin_user)
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

    def test_reset_password_without_template(self):
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
        }
        client = APIClient()
        response = client.post('/api/users/reset_password/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

    def test_unauthorized_reset_password_by_email(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'email': 'TestEmail1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = APIClient()
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

        os.remove(f'{settings.EMAIL_TEMPLATES_ROOT}email_template.html')

    def test_unauthorized_reset_password_by_username_and_email(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'email': 'TestEmail1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = APIClient()
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

        os.remove(f'{settings.EMAIL_TEMPLATES_ROOT}email_template.html')

    def test_unauthorized_update(self):
        updates = {
            'username': 'NewUsername1',
            'email': 'new@email.com',
            'password': 'NewPassword',
        }
        client = APIClient()
        response = client.put('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'new@email.com')

    def test_authorized_update(self):
        updates = {
            'username': 'NewUsername2',
            'email': 'new@email.com',
            'password': 'NewPassword',
        }

        client = self.authorize(self.second_user)
        response = client.put('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertNotEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'new@email.com')

    def test_owner_update(self):
        updates = {
            'username': 'NewUsername1',
            'email': 'new@email.com',
            'password': 'NewPassword',
        }
        client = self.authorize(self.first_user)
        response = client.put('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')

        client = self.authorize(self.first_user, username='NewUsername1')
        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_update(self):
        updates = {
            'username': 'NewUsername1',
            'email': 'new@email.com',
            'password': 'NewPassword',
        }
        client = self.authorize(self.admin_user)
        response = client.put('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).username, 'NewUsername1')
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'TestEmail1')

        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthorized_destroy(self):
        client = APIClient()
        response = client.delete('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_destroy(self):
        client = self.authorize(self.second_user)
        response = client.delete('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_destroy(self):
        client = self.authorize(self.first_user)
        response = client.delete('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(auth.get_user_model().objects.filter(id=1).exists())

    def test_admin_destroy(self):
        client = self.authorize(self.admin_user)
        response = client.delete('/api/users/{}/'.format(self.first_user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(auth.get_user_model().objects.filter(id=1).exists())

    def test_common_options(self):
        allowed_headers = ('Allow', 'GET, POST, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_detail_options(self):
        allowed_headers = ('Allow', 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')
        client = APIClient()
        response = client.options('/api/users/{}/'.format(self.first_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_verification_activation(self):
        sign_up_data = {
            'username': 'SignUpTestUsername',
            'password': 'blahasdblah',
            'email': 'signup@test.email',
        }

        client = APIClient()
        response = client.post('/api/users/', data=sign_up_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(tuple(response.data.keys()), self.basic_result_keys)

        new_user = auth.get_user_model().objects.get(id=response.data['id'])
        new_user.text_password = 'blahasdblah'
        activation_obj = Activation.objects.filter(user=new_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.authorize(new_user)

    def test_reset_password_activation(self):
        updates = {
            'email': 'TestEmail1',
            'password': 'NewPassword1',
        }

        client = APIClient()
        response = client.post('/api/users/reset_password/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Activation.objects.filter(user=auth.get_user_model().objects.get(id=self.first_user.id)).exists())

        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.post(f'/api/users/{activation_obj.user.id}/reset_password/{activation_obj.key}/confirm/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.authorize(self.first_user, password='NewPassword1')

    def test_owner_email_partial_update_activation(self):
        updates = {
            'email': 'NewEmail1@server.net',
        }

        client = self.authorize(self.first_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'NewEmail1@server.net')

    def test_admin_email_partial_update_activation(self):
        updates = {
            'email': 'NewEmail1@server.net',
        }

        client = self.authorize(self.admin_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'NewEmail1@server.net')

    def test_admin_email_partial_update_activation_with_template(self):
        data = File(open('media/email_templates/default_email_template.html', 'rb'))
        upload_file = SimpleUploadedFile('email_template.html', data.read(), content_type='multipart/form-data')
        updates = {
            'email': 'NewEmail1@server.net',
            'email_template': upload_file,
        }

        client = self.authorize(self.admin_user)
        response = client.patch(
            '/api/users/{}/'.format(self.first_user.id),
            data=updates,
            content_disposition='attachment; filename=email_template.html',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        activation_obj = Activation.objects.filter(user=self.first_user).first()
        response = client.get(f'/api/users/{activation_obj.user.id}/activation/{activation_obj.key}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(auth.get_user_model().objects.get(id=self.first_user.id).email, 'NewEmail1@server.net')

        os.remove(f'{settings.EMAIL_TEMPLATES_ROOT}email_template.html')

    def test_invalid_template(self):
        upload_file = SimpleUploadedFile('email_template.html', b'bla-bla-bla', content_type='multipart/form-data')
        updates = {
            'username': 'TestUsername1',
            'password': 'NewPassword1',
            'email_template': upload_file,
        }

        client = APIClient()
        response = client.post(
            '/api/users/reset_password/',
            data=updates,
            content_disposition='attachment; filename=email_template.html'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_partial_update(self):
        updates = {}
        client = self.authorize(self.first_user)
        response = client.patch('/api/users/{}/'.format(self.first_user.id), data=updates, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
