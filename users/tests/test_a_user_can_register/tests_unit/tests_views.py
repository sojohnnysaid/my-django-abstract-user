import re
from django.test.testcases import TestCase
from django.urls import reverse, reverse_lazy
from django.test import TestCase
from django.test import Client
from django.conf import settings as conf_settings

from unittest.mock import patch

from users import views, models, forms




class BaseTestCase(TestCase):

    def setUp(self):
        
        super().setUp()
        
        # register a user
        


    def register_user(self, name):
        data = {
            'email': f'{name}@gmail.com', 
            'first_name': name, 
            'password1': 'p@assW0rd', 
            'password2': 'p@assW0rd',}

        return Client().post(reverse('users:register'), data, follow=True)



class UserRegisterViewTest(BaseTestCase):

    def test_uses_MyAbstractUser(self):
        assert views.UsersRegisterView.model == models.MyAbstractUser
        
    def test_uses_UsersRegisterForm(self):
        assert views.UsersRegisterView.form_class == forms.UsersRegisterForm

    def test_uses_expected_template(self):
        assert views.UsersRegisterView.template_name == conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['register']

    def test_redirects_on_successful_post_request(self):
        expected_url = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']
        response = self.register_user('John')
        self.assertRedirects(response, expected_url)




class SendActivationLinkTest(BaseTestCase):
    
    
    @patch('users.services.send_mail')
    def test_calls_send_mail_service(self, mock_send_mail):
        self.register_user('John')
        mock_send_mail.assert_called_once()


    @patch('users.services.send_mail')
    def test_correct_arguments_passed_to_send_mail_service(self, mock_send_mail):
        self.register_user('John')
        link = mock_send_mail.call_args[0][1]
        url = re.search(r'http://.+/account-activation/\?uid=.+&token=.+$', link)
        mock_send_mail.assert_called_once_with(
            'Here is your activation link',
            url.group(0),
            'noreply@example.com',
            ['john@gmail.com'],
            fail_silently=False,
        )