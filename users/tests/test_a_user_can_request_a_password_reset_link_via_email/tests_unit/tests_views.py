import re
from urllib.parse import urlparse
from django.test.testcases import TestCase
from django.urls import reverse, reverse_lazy
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from django.core import mail
from django.test import Client
from django.conf import settings as conf_settings

from unittest.case import skip
from unittest.mock import patch

from users import forms



class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        email = 'john@gmail.com'
        password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=email, password=password)



class UsersPasswordResetRequestViewTest(BaseTestCase):

    def test_get_request_uses_expected_template(self):
        response = Client().get(reverse('users:password_request_reset_link'))
        self.assertTemplateUsed(response, conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['password_reset_request'])

    def test_uses_expected_form_class(self):
        response = Client().get(reverse('users:password_request_reset_link'))
        self.assertIsInstance(response.context_data['form'], forms.UsersPasswordResetRequestForm)

    @patch('users.views.services')
    def test_calls_send_password_reset_link_service_with_expected_arguments(self, mocked_services):
        
        response = Client().post(reverse('users:password_request_reset_link'), {'email': 'John@gmail.com'})
        request = response.wsgi_request
        mocked_services.send_password_reset_link.assert_called_once_with(request, self.user)

    def test_redirects_on_post_success(self):
        response = Client().post(reverse('users:password_request_reset_link'), {'email': 'John@gmail.com'})
        self.assertRedirects(response, str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']))
