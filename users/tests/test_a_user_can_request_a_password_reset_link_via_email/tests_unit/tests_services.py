from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model


from unittest.mock import patch

from users import services
from django.test import TestCase, Client




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        email = 'john@gmail.com'
        password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=email, password=password)


class SendPasswordResetLinkTest(BaseTestCase):

    def test_get_password_reset_link_returns_expected_url(self):
        request = RequestFactory().get('') # request path not important in this case
        expected_url = r'http://.+/users/password-reset/.+/.+$'
        generated_url = services.get_password_reset_link(request, self.user)
        self.assertRegex(generated_url, expected_url)

    
    @patch('users.services.get_password_reset_link')
    def test_send_password_reset_link_calls_get_password_reset_link(self, mock_get_password_reset_link):
        Client().post(reverse('users:password_request_reset_link'), {'email': self.user.email})
        mock_get_password_reset_link.assert_called_once()

    
    @patch('users.services.send_mail')
    def test_send_password_reset_link_calls_get_password_reset_link(self, mock_send_mail):
        Client().post(reverse('users:password_request_reset_link'), {'email': self.user.email})
        mock_send_mail.assert_called_once()