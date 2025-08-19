from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.models.user import Profile

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

    