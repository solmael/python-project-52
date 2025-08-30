import uuid

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.models import Label, Status, Task

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username=f'testuser_{uuid.uuid4().hex[:8]}',
            password='Newpass123+!'
        )
        self.other_user = User.objects.create_user(
            username=f'otheruser_{uuid.uuid4().hex[:8]}',
            password='Newpass123+!'
        )
        
        self.status = Status.objects.create(name='Тестовый статус')
        self.label = Label.objects.create(name='Тестовая метка')
        
        # create task
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание тестовой задачи',
            status=self.status,
            author=self.user,
            executor=self.other_user
        )
        self.task.labels.add(self.label)
    
    def test_task_list_view(self):
        # no login
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 302)
        
        # login
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        # open task list
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')
    
    def test_task_create_view(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        # open create
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        
        # data for
        data = {
            'name': 'Новая задача',
            'description': 'Описание новой задачи',
            'status': self.status.id,
            'executor': self.other_user.id,
            'labels': [self.label.id]
        }
        
        # post
        response = self.client.post(reverse('task_create'), data)
        self.assertRedirects(response, reverse('tasks'))
        
        # check task
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        new_task = Task.objects.get(name='Новая задача')
        self.assertEqual(new_task.author, self.user)
        self.assertEqual(new_task.status, self.status)
        self.assertEqual(new_task.executor, self.other_user)
        self.assertIn(self.label, new_task.labels.all())
    
    def test_task_update_view(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        # check update
        response = self.client.get(reverse('task_update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        
        # data for
        new_status = Status.objects.create(name='Новый статус')
        data = {
            'name': 'Обновленная задача',
            'description': 'Обновленное описание',
            'status': new_status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        }
        
        # post
        response = self.client.post(
            reverse('task_update', args=[self.task.id]), 
            data
            )
        self.assertRedirects(response, reverse('tasks'))
        
        # check data
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Обновленная задача')
        self.assertEqual(self.task.description, 'Обновленное описание')
        self.assertEqual(self.task.status, new_status)
        self.assertEqual(self.task.executor, self.user)
    
    def test_task_delete_view(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        # check delete
        response = self.client.get(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        
        # post
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        
        # check success
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
    
    def test_task_delete_by_non_author(self):
        # another user
        self.client.login(
            username=self.other_user.username, 
            password='Newpass123+!'
            )
        
        # try to delete task
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        
        # check error
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
    
    def test_task_detail_view(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        # check detail
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')
        self.assertContains(response, 'Описание тестовой задачи')
        self.assertContains(response, self.status.name)
        self.assertContains(response, self.other_user.username)
        self.assertContains(response, self.label.name)

    # filters
    def test_task_filtering_by_status(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        response = self.client.get(reverse('tasks'), {'status': self.status.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_filtering_by_executor(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        response = self.client.get(
            reverse('tasks'), {'executor': self.other_user.id}
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_filtering_by_label(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        response = self.client.get(reverse('tasks'), {'label': self.label.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_filtering_by_self_author(self):
        self.client.login(username=self.user.username, password='Newpass123+!')
        
        response = self.client.get(reverse('tasks'), {'self_author': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)