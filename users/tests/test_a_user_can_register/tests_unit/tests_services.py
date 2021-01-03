from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model


from unittest.mock import patch

from users import services




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()

    def register(self):
        return Client().post(reverse('users:register'), {
            'email': 'johnsmith@gmail.com',
            'first_name': 'John',
            'password1': 'p@assW0rd',
            'password2': 'p@assW0rd'
        })




class SendUserActivationLinkTest(BaseTestCase):

    @patch('users.services.get_activation_link')
    def test_get_activation_link_called(self, mock_get_activation_link):
        self.register()
        mock_get_activation_link.assert_called_once()


    def test_get_activation_link_returns_expected_url(self):
        email = 'johnsmith@gmail.com'
        response = self.register()
        request = response.wsgi_request
        user = get_user_model().objects.get(email=email)
        activation_link = services.get_activation_link(request, user)
        self.assertRegex(activation_link, r'http://.+/account-activation/\?uid=.+&token=.+$')


    @patch('users.services.send_mail')
    def test_calls_send_mail(self, mock_send_mail):
        email = 'johnsmith@gmail.com'
        response = self.register()
        mock_send_mail.assert_called_once()