from unittest import skip
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.User = get_user_model()



@skip
class MyViewTest(BaseTestCase):

    def test_view_returns_page_status_ok(self):
        response = Client().get(reverse(''))
        self.assertEqual(response.status_code, 200)