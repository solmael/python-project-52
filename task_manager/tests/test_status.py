from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from task_manager.models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.status = Status.objects.create(name='Test Status')
        self.client.login(username='testuser', password='testpass')
    
    def test_status_list_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)
    
    def test_status_create_view(self):
        data = {'name': 'New Status'}
        response = self.client.post(reverse('status_create'), data)
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())
    
    def test_status_update_view(self):
        data = {'name': 'Updated Status'}
        response = self.client.post(reverse('status_update', args=[self.status.id]), data)
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')
    
    def test_status_delete_view(self):
        response = self.client.post(reverse('status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())