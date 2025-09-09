import uuid

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.models import Status, Task

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = f'testuser_{uuid.uuid4().hex[:8]}'
        self.password = 'Newpass123+!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'Newpass123+!',
            'password2': 'Newpass123+!'
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_view(self):
        self.client.login(username=self.username, password=self.password)
        
        data = {
            'username': self.username,
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.post(
            reverse('user_update', args=[self.user.id]), 
            data
            )
        self.assertRedirects(response, reverse('users'))
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_delete_view(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users'))
        
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

    def test_user_delete_with_tasks(self):
        self.client.login(username=self.username, password=self.password)
        
        task_data = {
            'name': 'Test Task',
            'status': Status.objects.create(name='New'),
            'author': self.user
        }
        Task.objects.create(**task_data)
        
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users'))
        
        # User not deleted
        self.assertTrue(User.objects.filter(id=self.user.id).exists())
        
        # check massage
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(
            "Невозможно удалить пользователя" in str(m) for m in messages)
            )
    
    def test_update_other_user_profile(self):
        self.client.login(username=self.username, password=self.password)
        
        # another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='Otherpass123+!'
        )
        
        data = {
            'username': 'otheruser',
            'first_name': 'Hacked',
            'last_name': 'User'
        }
        
        response = self.client.post(
            reverse('user_update', args=[other_user.id]), 
            data
        )
        
        self.assertRedirects(response, reverse('users'))
        
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(
            "У вас нет прав для изменения" in str(m) for m in messages)
            )
        
        # chech data
        other_user.refresh_from_db()
        self.assertNotEqual(other_user.first_name, 'Hacked')

    def test_delete_other_user_profile(self):
        self.client.login(username=self.username, password=self.password)
        
        # another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='Otherpass123+!'
        )
        
        response = self.client.post(
            reverse('user_delete', args=[other_user.id])
        )
        
        self.assertRedirects(response, reverse('users'))
        
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(
            "У вас нет прав для изменения" in str(m) for m in messages)
            )
        
        # check user not delete
        self.assertTrue(User.objects.filter(id=other_user.id).exists())

    def test_update_profile_without_login(self):
        response = self.client.post(
            reverse('user_update', args=[self.user.id]),
            {'first_name': 'Updated'}
        )
        
        self.assertRedirects(
            response, 
            f"{reverse('login')}?next={reverse(
                'user_update', 
                args=[self.user.id])}"
        )
        
        # check data no change
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.first_name, 'Updated')

    def test_user_create_with_existing_username(self):
        data = {
            'username': self.username,
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'Newpass123+!',
            'password2': 'Newpass123+!'
        }
        response = self.client.post(reverse('user_create'), data)
    
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context['form'], 
            'username', 
            'Пользователь с таким именем уже существует.'
        )

    def test_delete_own_profile(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        
        self.assertRedirects(response, reverse('users'))
        
        # check user delete
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)
        
        # check message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь успешно удален")

    def test_user_create_with_weak_password(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'password',
            'password2': 'password'
        }
        response = self.client.post(reverse('user_create'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.has_error('password2'))
        self.assertFalse(form.is_valid())
    
    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_success(self):
        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('home'))
        
        response = self.client.get(reverse('home'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)