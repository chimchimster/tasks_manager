import dataclasses

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import *


class ApiViewTestCase(TestCase):

    fixtures = ['test_data.json']

    def setUp(self):

        self.username = 'test_user'
        self.password = 'test_password'
        self.email = 'test_email@example.com'

        register_response = self.client.post(
            reverse('tasks_api:user-register'),
            data={'username': self.username, 'email': self.email, 'password': self.password},
            content_type='application/json',
        )
        self.assertEqual(register_response.status_code, 201)

        token_response = self.client.post(
            reverse('tasks_api:token_get'),
            data={'username': self.username, 'password': self.password},
            content_type='application/json',
        )
        self.assertEqual(token_response.status_code, 200)
        self.token = token_response.json().get('access')

    def test_get_board_by_id(self):

        board_response = self.client.get(
            reverse('tasks_api:board', kwargs={'pk': 1}),
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )

        self.assertEquals(
            board_response.status_code,
            200,
            'Борд не был получен. Код %s' % board_response.status_code
        )

        self.assertEquals(
            board_response.json().get('title'),
            'Development backend.',
            'Название борда не совпадает.',
        )

    def test_create_board(self):

        board_response = self.client.post(
            reverse('tasks_api:create_board'),
            data={'title': 'Test board', 'description': 'This is test board.'},
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )

        self.assertEquals(
            board_response.status_code,
            201,
            'Борд не был создан. Код %s' % board_response.status_code,
        )

    def test_update_board(self):

        board_response = self.client.put(
            reverse('tasks_api:board', kwargs={'pk': 1}),
            data={'title': 'New board title'},
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )
        self.assertEquals(
            board_response.status_code,
            200,
            'Название борда не изменилось.',
        )

    def test_remove_board(self):

        board_response = self.client.delete(
            reverse('tasks_api:board', kwargs={'pk': 1}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )
        self.assertEquals(
            board_response.status_code,
            403,
            'Невозможно удалить Борд.',
        )

    def test_get_task(self):

        task_response = self.client.get(
            reverse('tasks_api:task', kwargs={'pk': 1}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )
        self.assertEquals(
            task_response.status_code,
            200,
            'Таск не был получен. Код %s' % task_response.status_code,
        )
        title = task_response.json().get('title')
        self.assertEquals(
            task_response.json().get('title'),
            'Do homework!',
            'Получен неверный таск. Код %s' % title,
        )

    def test_create_task(self):

        new_task_data = {
            'title': 'New Task',
            'description': 'This is a new task.',
            'board_id': 1,
            'priority': 1,
            'tags': [1, 2, 3],
            'attachment': None,
            'due_to': '2024-12-24',
            'status': 'to_do',
            'participants': [1, 2, 3]
        }

        task_response = self.client.post(
            reverse('tasks_api:create_task'),
            data=new_task_data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )
        self.assertEquals(
            task_response.status_code,
            201,
            'Таск не был создан. Код %s' % task_response.status_code,
        )

        self.assertEquals(
            task_response.json().get('title'),
            new_task_data['title'],
            'Название таска не совпадает.',
        )

    def test_update_task_status(self):

        updated_task_data = {
            'status': 'in_progress'
        }

        task_response = self.client.put(
            reverse('tasks_api:task', kwargs={'pk': 1}),
            data=updated_task_data,
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )

        self.assertEquals(
            task_response.status_code,
            403,
            'Только участники могут обновлять статус таска.'
        )

    def test_remove_task(self):

        task_response = self.client.delete(
            reverse('tasks_api:task', kwargs={'pk': 1}),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer %s' % self.token,
        )

        self.assertEquals(
            task_response.status_code,
            403,
            'Невозмонжно удалить таск, если вы не администратор.'
        )
