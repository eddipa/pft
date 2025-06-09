from django.urls import reverse
from django.test import TestCase

class URLAccessTest(TestCase):
    def test_redirect_for_anonymous_dashboard(self):
        response = self.client.get(reverse('finance:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
