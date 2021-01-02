from unittest import skip
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings as conf_settings




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.User = get_user_model()




class LogoutTest(BaseTestCase):

    def test_logout_redirects_user_to_expected_page(self):
        response = Client().get(reverse('users:logout'), follow=True)
        self.assertRedirects(response, str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']))