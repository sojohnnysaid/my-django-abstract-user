from urllib.parse import urlparse

from unittest.case import skip

from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.conf import settings as conf_settings
from django.urls import resolve, reverse

from users import services, views





class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class RegisterURLTest(BaseTestCase):

    def test_calls_correct_view(self):
        expected_class = views.UsersRegisterView
        name = 'users:register'
        resolver_match = resolve(reverse(name))
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)
    



class RegisterFormSubmittedURLTest(BaseTestCase):


    def test_calls_correct_view(self):
        expected_class = views.UsersRegisterView
        name = 'users:register'
        resolver_match = resolve(reverse(name))
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)