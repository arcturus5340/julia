from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.contrib.auth.models import Group
from django.contrib import auth
from contest.models import Contest, Task, TestCase

import datetime


class ContestTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        verified_users_group = Group.objects.create(name='Verified Users')
        contest1 = Contest.objects.create(
            title='TestTitle1',
            description='TestDescription1',
        )
        contest2 = Contest.objects.create(
            title='TestTitle2',
            description='TestDescription2',
        )
        Contest.objects.create(
            title='TestTitle3',
            description='TestDescription3',
        )
        task = Task.objects.create(
            title='TestTitle1',
            content='TestContent1',
            contest=contest1,
            ml=512*2**20,
            tl=5,
            _order=0,
        )
        TestCase.objects.create(
            input='0 0',
            output='0',
            task=task,
        )
        cls.user =auth.get_user_model().objects.create(
            username='TestUsername',
            email='TestEmail',
        )
        cls.user.set_password('TestPassword')
        cls.user.text_password = 'TestPassword'
        cls.user.groups.add(verified_users_group)
        cls.user.save()
        cls.admin = auth.get_user_model().objects.create(
            username='TestAdminUsername',
            email='TestAdminEmail',
            is_staff=True,
        )
        cls.admin.set_password('TestAdminPassword')
        cls.admin.text_password = 'TestAdminPassword'
        cls.admin.groups.add(verified_users_group)
        cls.admin.save()
        cls.result_keys = ('id', 'title', 'description', 'tasks', 'start_time', 'duration')
        cls.task_result_keys = ('id', 'title', 'content', 'contest', 'tl', 'ml', 'samples')

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
        response = client.head('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_head(self):
        client = self.authorize(self.user)
        response = client.head('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_head(self):
        client = self.authorize(self.admin)
        response = client.head('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_list(self):
        client = APIClient()
        response = client.get('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_authorized_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_admin_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        for result in response.data['results']:
            self.assertEqual(tuple(result.keys()), self.result_keys)

    def test_unauthorized_tasks_list(self):
        client = APIClient()
        response = client.get('/api/contests/1/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.task_result_keys)

    def test_authorized_tasks_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/1/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.task_result_keys)

    def test_admin_tasks_list(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/1/tasks/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.task_result_keys)

    def test_list_filter(self):
        client = APIClient()
        response = client.get('/api/contests/?title=TestTitle1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_search(self):
        client = APIClient()
        response = client.get('/api/contests/?search=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unauthorized_create(self):
        new_contest_data = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': datetime.datetime.now() + datetime.timedelta(hours=1),
            'duration': datetime.timedelta(hours=2)
        }

        client = APIClient()
        response = client.post('/api/contests/', data=new_contest_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_create(self):
        new_contest_data = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': datetime.datetime.now() + datetime.timedelta(hours=1),
            'duration': datetime.timedelta(hours=2)
        }

        client = self.authorize(self.user)
        response = client.post('/api/contests/', data=new_contest_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create(self):
        new_contest_data = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).second,
            'duration': datetime.timedelta(hours=2).seconds
        }

        client = self.authorize(self.admin)
        response = client.post('/api/contests/', data=new_contest_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contest.objects.count(), 4)
        self.assertEqual(Contest.objects.get(id=4).title, 'NewTestTitle')
        self.assertEqual(Contest.objects.get(id=4).description, 'NewTestDescription')
        self.assertEqual(Contest.objects.get(id=4).duration.seconds, 7200)


    def test_unauthorized_retrieve(self):

        client = APIClient()
        response = client.get('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_authorized_retrieve(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_admin_retrieve(self):
        client = self.authorize(self.user)
        response = client.get('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_non_existent_retrieve(self):
        client = APIClient()
        response = client.get('/api/contests/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)\

    def test_unauthorized_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }

        client = APIClient()
        response = client.patch('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Contest.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Contest.objects.get(id=1).description, 'TestDescription1')

    def test_authorized_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }

        client = self.authorize(self.user)
        response = client.patch('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Contest.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Contest.objects.get(id=1).description, 'TestDescription1')

    def test_admin_partial_update(self):
        updates = {
            'title': 'NewTitle1',
        }
        client = self.authorize(self.admin)
        response = client.patch('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Contest.objects.get(id=1).title, 'NewTitle1')
        self.assertEqual(Contest.objects.get(id=1).description, 'TestDescription1')
        self.assertEqual(tuple(response.data.keys()), self.result_keys)

    def test_admin_partial_wrong_task_update(self):
        updates = {
            'tasks': 0,
        }

        client = self.authorize(self.admin)
        response = client.patch('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_update(self):
        updates = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': datetime.datetime.now() + datetime.timedelta(hours=1),
            'duration': datetime.timedelta(hours=2)
        }
        client = APIClient()
        response = client.put('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Contest.objects.get(id=1).title, 'NewTestTitle')
        self.assertNotEqual(Contest.objects.get(id=1).description, 'NewTestDescription')

    def test_authorized_update(self):
        updates = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': datetime.datetime.now() + datetime.timedelta(hours=1),
            'duration': datetime.timedelta(hours=2)
        }

        client = self.authorize(self.user)
        response = client.put('/api/contests/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Contest.objects.get(id=1).title, 'NewTestTitle')
        self.assertNotEqual(Contest.objects.get(id=1).description, 'NewTestDescription')

    def test_admin_update(self):
        task = Task.objects.create(
            title='TestTitle1',
            content='TestContent1',
            contest=Contest.objects.get(id=3),
            ml=512*2**20,
            tl=5,
            _order=1,
        )
        updates = {
            'title': 'NewTestTitle',
            'description': 'NewTestDescription',
            'start_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).second,
            'duration': datetime.timedelta(hours=2)
        }
        client = self.authorize(self.admin)
        response = client.put('/api/contests/2/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(response.data)
        self.assertEqual(Contest.objects.get(id=2).title, 'NewTestTitle')
        self.assertEqual(Contest.objects.get(id=2).description, 'NewTestDescription')

    def test_unauthorized_destroy(self):
        client = APIClient()
        response = client.delete('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_destroy(self):
        client = self.authorize(self.user)
        response = client.delete('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_destroy_contest_with_tasks(self):
        client = self.authorize(self.admin)
        response = client.delete('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_admin_destroy_contest(self):
        client = self.authorize(self.admin)
        response = client.delete('/api/contests/3/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_common_options(self):
        allowed_headers = ('Allow', 'GET, POST, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/contests/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_detail_options(self):
        allowed_headers = ('Allow', 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/contests/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def send_solution(self, user, task):
        data = File(open('contest/tests/src/one.py', 'rb'))
        upload_file = SimpleUploadedFile('one.py', data.read(), content_type='multipart/form-data')
        solution_data = {
            'code': upload_file,
            'lang': 'python3',
            'task': task,
        }

        client = self.authorize(user)
        response = client.post(
            '/api/solutions/',
            data=solution_data,
            content_disposition="attachment; filename=one.py"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_results(self):
        self.send_solution(self.user, 1)
        self.send_solution(self.user, 1)
        self.send_solution(self.admin, 1)

        client = APIClient()
        response = client.get('/api/contests/1/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
