from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()

class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.profile = Profile.objects.create(user=self.user, full_name='Test User')

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view(self):
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'Newpass123+',
            'password2': 'Newpass123+'
        }
        response = self.client.post(reverse('user_create'), data)
        self.assertRedirects(response, reverse('login'))

    def test_user_update_view(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'username': 'testuser',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.post(reverse('user_update', args=[self.user.id]), data)
        self.assertRedirects(response, reverse('users'))
        
        # refresh_data
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users'))
        
        # delete_user
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)