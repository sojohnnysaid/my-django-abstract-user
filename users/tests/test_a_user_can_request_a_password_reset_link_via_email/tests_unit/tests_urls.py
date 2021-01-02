from urllib.parse import urlparse

from unittest.case import skip
from django.test import TestCase
from django.test.client import Client, RequestFactory
from django.urls import resolve, reverse

from users import services, views




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class PasswordResetRequestURLTest(BaseTestCase):        

    def test_resolves_to_correct_view(self):
        expected_class = views.UsersPasswordResetRequestView
        name = 'users:password_request_reset_link'
        resolver_match = resolve(reverse(name))
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)