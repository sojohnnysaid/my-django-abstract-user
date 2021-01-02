from django.test import TestCase, Client
from django.urls import reverse

from users import views



class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class LoginUrlTest(BaseTestCase):

    def test_login_url_calls_expected_class(self):
        response = Client().get(reverse('users:login'))
        self.assertIsInstance(response.context_data['view'], views.UsersLoginView)
