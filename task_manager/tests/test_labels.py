from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Label, Status, Task


class LabelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.label = Label.objects.create(name='Test Label')
        self.task = Task.objects.create(
            name='Test Task',
            author=self.user,
            status=Status.objects.create(name='New')
        )
        self.task.labels.add(self.label)

    def test_label_list_view(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')

    def test_create_label(self):
        response = self.client.post(reverse('label_create'), {'name': 'New Label'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_delete_used_label(self):
        response = self.client.post(reverse('label_delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())