from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass')
        self.client.login(email='user@example.com', password='testpass')

    def test_dashboard_view(self):
        response = self.client.get(reverse('finance:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
