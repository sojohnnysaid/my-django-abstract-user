from unittest import skip
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.email = 'john@gmail.com'
        self.password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.user.is_active = False
        self.user.save()



class ResendAccountActivationLinkLoginViewTest(BaseTestCase):

    def test_shows_inactive_error_message_when_inactive_user_submits_login_using_django_messages_instead_of_form_field_errors(self):
        data = {'username': self.email, 'password': self.password}
        response = Client().post(reverse('users:login'), data, follow=True)
        link = reverse_lazy('users:account_activation_request')
        expected_message = mark_safe(f'Account has not been activated! <a href={link}>Click here to resend activation link</a>')
        self.assertContains(response, expected_message)


    def test_will_not_show_form_field_error(self):
        data = {'username': self.email, 'password': self.password}
        response = Client().post(reverse('users:login'), data, follow=True)
        self.assertNotContains(
            response,
            'This account is inactive'
        )

    

class AccountActivationRequestViewTest(BaseTestCase):

    def test_view_returns_page_status_ok(self):
        response = Client().get(reverse('users:account_activation_request'))
        self.assertEqual(response.status_code, 200)
