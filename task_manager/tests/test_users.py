import uuid

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

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