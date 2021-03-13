from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib import auth
from django.contrib.auth.models import Group
from contest.models import Contest, Task, TestCase, Solution

import datetime


class SolutionTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        verified_users_group = Group.objects.create(name='Verified Users')
        cls.first_user = auth.get_user_model().objects.create(
            username='TestUsername1',
            email='TestEmail1',
        )
        cls.first_user.set_password('TestPassword1')
        cls.first_user.text_password = 'TestPassword1'
        cls.first_user.groups.add(verified_users_group)
        cls.first_user.save()
        cls.second_user = auth.get_user_model().objects.create(
            username='TestUsername2',
            email='TestEmail2',
        )
        cls.second_user.set_password('TestPassword2')
        cls.second_user.text_password = 'TestPassword2'
        cls.second_user.groups.add(verified_users_group)
        cls.second_user.save()
        cls.admin_user = auth.get_user_model().objects.create(
            username='TestAdminUsername',
            email='TestAdminEmail',
            is_staff=True,
        )
        cls.admin_user.set_password('TestAdminPassword')
        cls.admin_user.text_password = 'TestAdminPassword'
        cls.admin_user.groups.add(verified_users_group)
        cls.admin_user.save()
        contest = Contest.objects.create(
            title='TestContest',
            description='TestDescription',
            start_time=datetime.datetime.now(),
            duration=datetime.timedelta(hours=2),
        )
        task = Task.objects.create(
            title='TestTaskAdd',
            content='TestContentAdd',
            contest=contest,
            ml=2**28,
            tl=2,
            _order=0,
        )
        TestCase.objects.create(
            task=task,
            input='0 0',
            output='0',
        )
        TestCase.objects.create(
            task=task,
            input='0 1',
            output='1',
        )
        TestCase.objects.create(
            task=task,
            input='1 1',
            output='2',
        )
        cls.create_solution_response = cls.create_solution(cls)
        cls.list_result_keys = ('id', 'author', 'task', 'status', 'dispatch_time')
        cls.retrieve_result_keys = ('id', 'author', 'task', 'status', 'dispatch_time')

    def tearDown(self):
        # for file in os.listdir(settings.CODE_ROOT):
        #     if file.startswith('TestUsername1'):
        #         os.remove(f'{settings.CODE_ROOT}{file}')
        pass

    @classmethod
    def authorize(cls, user):
        sign_in_data = {
            'username': user.username,
            'password': user.text_password,
        }

        client = APIClient()
        response = client.post('/api/token-auth', data=sign_in_data, format='json')
        token = response.data['token']
        client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        return client

    def create_solution(cls):
        data = File(open('contest/tests/src/one.py', 'rb'))
        upload_file = SimpleUploadedFile('one.py', data.read(), content_type='multipart/form-data')

        response = cls.authorize(cls.first_user).post(
            '/api/solutions/',
            data={'code': upload_file, 'lang': 'python3', 'task': 1},
            content_disposition="attachment; filename=one.py"
        )
        return response

    def test_unauthorized_head(self):
        client = APIClient()
        response = client.head('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_head(self):
        client = self.authorize(self.first_user)
        response = client.head('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_head(self):
        client = self.authorize(self.admin_user)
        response = client.head('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_list(self):
        client = APIClient()
        response = client.get('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.list_result_keys)

    def test_authorized_list(self):
        client = self.authorize(self.first_user)
        response = client.get('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.list_result_keys)

    def test_admin_list(self):
        client = self.authorize(self.first_user)
        response = client.get('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(tuple(response.data['results'][0].keys()), self.list_result_keys)

    def test_list_filter_username(self):
        client = APIClient()
        response = client.get('/api/solutions/?username=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


    def test_list_filter_task(self):
        client = APIClient()
        response = client.get('/api/solutions/?task=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_list_filter_status(self):
        client = APIClient()
        response = client.get('/api/solutions/?status=WA')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_empty_list_filter_status(self):
        client = APIClient()
        response = client.get('/api/solutions/?status=OK')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_list_search(self):
        client = APIClient()
        response = client.get('/api/solutions/?search=1')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unauthorized_create(self):
        data = File(open('contest/tests/src/one.py', 'rb'))
        upload_file = SimpleUploadedFile('one.py', data.read(), content_type='multipart/form-data')
        solution_data = {
            'code': upload_file,
            'lang': 'python3',
            'task': 1,
        }

        client = APIClient()
        response = client.post(
            '/api/solutions/',
            data=solution_data,
            content_disposition="attachment; filename=one.py"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_create(self):
        data = File(open('contest/tests/src/one.cpp', 'rb'))
        upload_file = SimpleUploadedFile('one.py', data.read(), content_type='multipart/form-data')
        solution_data = {
            'code': upload_file,
            'lang': 'cpp11',
            'task': 1,
        }
        expected_response = {
            'id':2,
            'author': 1,
            'details': {
                'input': {0: '0 0', 1: '0 1'},
                'output': {0: '0', 1: '1'},
                'program_output': {0: '0', 1: '1', 2: 'Ooops!'},
                'status': {0: 'OK', 1: 'OK', 2: 'WA'}
            },
            'status': 'WA',
            'task': 1
        }

        client = self.authorize(self.first_user)
        response = client.post(
            '/api/solutions/',
            data=solution_data,
            content_disposition="attachment; filename=one.py"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details'], expected_response['details'])

    def test_unauthorized_retrieve(self):
        client = APIClient()
        response = client.get('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.retrieve_result_keys)

    def test_authorized_retrieve(self):
        client = self.authorize(self.second_user)
        response = client.get('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.retrieve_result_keys)

    def test_owner_retrieve(self):

        client = self.authorize(self.first_user)
        response = client.get('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.retrieve_result_keys)

    def test_admin_retrieve(self):
        client = self.authorize(self.admin_user)
        response = client.get('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tuple(response.data.keys()), self.retrieve_result_keys)

    def test_non_existent_retrieve(self):
        client = self.authorize(self.admin_user)
        response = client.get('/api/solutions/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_partial_update(self):
        updates = {
            'status': 'OK',
        }

        client = APIClient()
        response = client.patch('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_partial_update(self):
        updates = {
            'status': 'OK',
        }

        client = self.authorize(self.second_user)
        response = client.patch('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_partial_update(self):
        updates = {
            'status': 'OK',
        }

        client = self.authorize(self.first_user)
        response = client.patch('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_partial_update(self):
        updates = {
            'author': 1,
            'task': 1,
            'status': 'OK',
        }

        client = self.authorize(self.admin_user)
        response = client.patch('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_update(self):
        updates = {
            'author': 1,
            'task': 1,
            'status': 'OK',
        }

        client = APIClient()
        response = client.put('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(Solution.objects.get(id=1).status, 'OK')

    def test_authorized_update(self):
        updates = {
            'author': 1,
            'task': 1,
            'status': 'OK',
        }

        client = self.authorize(self.second_user)
        response = client.put('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Solution.objects.get(id=1).status, 'OK')

    def test_owner_update(self):
        updates = {
            'author': 1,
            'task': 1,
            'status': 'OK',
        }

        client = self.authorize(self.first_user)
        response = client.put('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Solution.objects.get(id=1).status, 'OK')

    def test_admin_update(self):
        updates = {
            'author': 1,
            'task': 1,
            'status': 'OK',
        }

        client = self.authorize(self.admin_user)
        response = client.put('/api/solutions/1/', data=updates, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Solution.objects.get(id=1).status, 'OK')

    def test_unauthorized_destroy(self):
        client = APIClient()
        response = client.delete('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_destroy(self):
        client = self.authorize(self.second_user)
        response = client.delete('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_destroy(self):
        client = self.authorize(self.first_user)
        response = client.delete('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_destroy(self):
        client = self.authorize(self.admin_user)
        response = client.delete('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_common_options(self):
        allowed_headers = ('Allow', 'GET, POST, HEAD, OPTIONS')

        client = APIClient()
        response = client.options('/api/solutions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_detail_options(self):
        allowed_headers = ('Allow', 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')
        client = APIClient()
        response = client.options('/api/solutions/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response._headers['allow'], allowed_headers)

    def test_code_fetch_during_contest(self):
        client = self.authorize(self.first_user)
        response = client.get(f'/{settings.CODE_DIR}{self.create_solution_response.data["code"].split("/")[-1]}')

    def test_speedy1(self):
        data = File(open('contest/tests/src/one.ssf', 'rb'))
        upload_file = SimpleUploadedFile('one.ssf', data.read(), content_type='multipart/form-data')

        response = self.authorize(self.first_user).post(
            '/api/solutions/',
            data={'code': upload_file, 'lang': 'speedy1', 'task': 1},
            content_disposition="attachment; filename=one.ssf"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details']['status'][2], 'WA')
