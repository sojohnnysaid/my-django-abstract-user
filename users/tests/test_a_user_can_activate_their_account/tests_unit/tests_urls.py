from urllib.parse import urlparse

from unittest.case import skip
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls import resolve, reverse_lazy

from users import services, views



class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class AccountActivationURLTest(BaseTestCase):

    def test_calls_correct_view(self):
        expected_class = views.UsersAccountActivationView
        name = 'users:account_activation'
        resolver_match = resolve(reverse_lazy(name))
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)