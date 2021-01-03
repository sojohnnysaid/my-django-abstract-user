from unittest import skip
from unittest.mock import patch, Mock

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe

from users import forms



class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.email = 'john@gmail.com'
        self.password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.user.is_active = False
        self.user.save()




class UserCanRequestAccountActivationLinkFormTest(BaseTestCase):

    def test_when_user_not_active_raises_validation_error(self):
        data = {'username': self.email, 'password': self.password}
        response = Client().post(reverse('users:login'), data, follow=True)
        link = reverse_lazy('users:account_activation_request')
        error_message = mark_safe(
                    f"Account has not been activated! <a href={link}>Click here to resend activation link</a>")
        self.assertFormError(response, 'form', 'username', error_message)