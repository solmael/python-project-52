from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            full_name='Test User'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        data = {
            'username': 'newuser',
            'full_name': 'New User',
            'password1': 'newpass',
            'password2': 'newpass'
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'username': 'updateduser',
            'full_name': 'Updated User'
        }
        response = self.client.post(reverse('user_update', args=[self.user.id]), data)
        self.assertRedirects(response, reverse('users'))

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users'))