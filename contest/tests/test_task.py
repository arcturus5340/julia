from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib import auth

from django.contrib.auth.models import Group
from contest.models import Contest, Task, TestCase

import datetime


class TaskTestCase(APITestCase):
    def setUp(self):
        verified_users_group = Group.objects.create(name='Verified Users')
        contest = Contest.objects.create(
            title='TestTitle1',
            description='TestDescription1',
            start_time=datetime.datetime.now(),
            duration=datetime.timedelta(hours=2),
        )
        Contest.objects.create(
            title='TestTitle2',
            description='TestDescription2',
            start_time=datetime.datetime.now(),
            duration=datetime.timedelta(hours=2),
        )
        past_contest = Contest.objects.create(
            title='Past Contest',
            description='Past Contest',
            start_time=datetime.datetime.now() - datetime.timedelta(hours=2),
            duration=datetime.timedelta(hours=1),
        )
        future_contest = Contest.objects.create(
            title='Future Contest',
            description='Future Contest',
            start_time=datetime.datetime.now() + datetime.timedelta(hours=2),
            duration=datetime.timedelta(hours=1),
        )
        Task.objects.create(
            title='TestTitle1',
            content='TestContent1',
            contest=contest,
            ml=512,
            tl=5,
            _order=0,
        )
        Task.objects.create(
            title='TestTitle2',
            content='TestContent2',
            contest=contest,
            ml=512,
            tl=5,
            _order=1,
        )
        Task.objects.create(
            title='TestTitle3',
            content='TestContent3',
            contest=contest,
            ml=512,
            tl=5,
            _order=2,
        )
        Task.objects.create(
            title='PastTitle',
            content='PastContent',
            contest=past_contest,
            ml=512,
            tl=5,
            _order=0,
        )
        Task.objects.create(
            title='FutureTitle1',
            content='FutureContent1',
            contest=future_contest,
            ml=512,
            tl=5,
            _order=0,
        )
        Task.objects.create(
            title='FutureTitle2',
            content='FutureContent2',
            contest=future_contest,
            ml=512,
            tl=5,
            _order=1,
        )
        self.user = auth.get_user_model().objects.create(
            username='TestUsername',
            email='TestEmail',
        )
        self.user.set_password('TestPassword')
        self.user.text_password = 'TestPassword'
        self.user.groups.add(verified_users_group)
        self.user.save()
        self.admin = auth.get_user_model().objects.create(
            username='TestAdminUsername',
            email='TestAdminEmail',
            is_staff=True,
        )
        self.admin.set_password('TestAdminPassword')
        self.admin.text_password = 'TestAdminPassword'
        self.admin.groups.add(verified_users_group)
        self.admin.save()
        self.result_keys = ('id', 'title', 'content', 'contest', 'tl', 'ml', 'samples')

    @staticmethod
    def authorize(user):
        sign_in_data = {
            'username': user.username,
            'password': user.text_password,
        }

        client = APIClient()
        response = client.post('/api/token-auth', data=sign_in_data, format='json')
        token = response.data['token']
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        return client

    def test_unauthorized_head(self):
        client = APIClient()
        response = client.head('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_head(self):
        client = self.authorize(self.user)
        response = client.head('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_head(self):
        client = self.authorize(self.admin)
        response = client.head('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_list(self):
        client = APIClient()
        response = client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_authorized_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_admin_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_list_filter(self):
        client = APIClient()
        response = client.get('/api/tasks/?title=TestTitle1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_search(self):
        client = APIClient()
        response = client.get('/api/tasks/?search=Content1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_unauthorized_create(self):
        new_task_data = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 1,
        }

        client = APIClient()
        response = client.post('/api/tasks/', data=new_task_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_create(self):
        new_task_data = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 1,
        }

        client = self.authorize(self.user)
        response = client.post('/api/tasks/', data=new_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create(self):
        new_task_data = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 1,
            '_order': 3,
            'test_cases': [
                {
                    'input': '0 0',
                    'output': '0',
                },
                {
                    'input': '0 1',
                    'output': '1',
                },
                {
                    'input': '1 1',
                    'output': '1',
                }
            ]
        }

        client = self.authorize(self.admin)
        response = client.post('/api/tasks/', data=new_task_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 7)
        self.assertEqual(Task.objects.get(id=7).title, 'NewTestTitle')
        self.assertEqual(Task.objects.get(id=7).content, 'NewTestContent')
        self.assertEqual(Task.objects.get(id=7).contest, Contest.objects.get(id=1))
        self.assertEqual(Task.objects.get(id=7).ml, 2**28)
        self.assertEqual(Task.objects.get(id=7).tl, 2)

    def test_unauthorized_retrieve(self):
        client = APIClient()
        response = client.get('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_authorized_retrieve(self):


        client = self.authorize(self.user)
        response = client.get('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_admin_retrieve(self):
        client = self.authorize(self.user)
        response = client.get('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_non_existent_retrieve(self):
        client = APIClient()
        response = client.get('/api/tasks/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)\

    def test_unauthorized_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }

        client = APIClient()
        response = client.patch('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Task.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Task.objects.get(id=1).content, 'TestContent1')

    def test_authorized_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }

        client = self.authorize(self.user)
        response = client.patch('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Task.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Task.objects.get(id=1).content, 'TestContent1')

    def test_admin_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }


        client = self.authorize(self.admin)
        response = client.patch('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Task.objects.get(id=1).content, 'TestContent1')
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_admin_partial_wrong_contest_update(self):
        updates = {
            'contest': 0,
        }

        client = self.authorize(self.admin)
        response = client.patch('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(Task.objects.get(id=1).contest.id, 0)

    def test_unauthorized_update(self):
        updates = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 2,
        }
        client = APIClient()
        response = client.put('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Task.objects.get(id=1).title, 'NewTestTitle')
        self.assertNotEqual(Task.objects.get(id=1).content, 'NewTestContent')
        self.assertNotEqual(Task.objects.get(id=1).contest.id, 2)

    def test_authorized_update(self):
        updates = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 2,
        }

        client = self.authorize(self.user)
        response = client.put('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Task.objects.get(id=1).title, 'NewTestTitle')
        self.assertNotEqual(Task.objects.get(id=1).content, 'NewTestContent')
        self.assertNotEqual(Task.objects.get(id=1).contest.id, 2)

    def test_admin_update(self):
        updates = {
            'title': 'NewTestTitle',
            'content': 'NewTestContent',
            'contest': 2,
            '_order': 0,
        }
        client = self.authorize(self.admin)
        response = client.put('/api/tasks/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(Task.objects.get(id=1).title, 'NewTestTitle')
        self.assertEqual(Task.objects.get(id=1).content, 'NewTestContent')
        self.assertEqual(Task.objects.get(id=1).contest.id, 2)

    def test_unauthorized_destroy(self):
        client = APIClient()
        response = client.delete('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_destroy(self):
        client = self.authorize(self.user)
        response = client.delete('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_destroy(self):
        client = self.authorize(self.admin)
        response = client.delete('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_common_options(self):
        allowed_headers = ('Allow', 'GET, POST, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_detail_options(self):
        allowed_headers = ('Allow', 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/tasks/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)
