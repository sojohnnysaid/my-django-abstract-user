from urllib.parse import urlparse

from unittest.case import skip

from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model

from users import services, views




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        email = 'john@gmail.com'
        password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=email, password=password)




class PasswordResetURLTest(BaseTestCase):
    

    def test_resolves_to_correct_view(self):
        request = RequestFactory().get('') # request path not important in this case
        url = services.get_password_reset_link(request, self.user)
        path = urlparse(url).path
        
        expected_class = views.UsersPasswordResetView
        resolver_match = resolve(path)
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)