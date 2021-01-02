from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings as conf_settings



class BaseTestCase(TestCase):

    def setUp(self):
        self.email = 'john@gmail.com'
        self.password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.user.is_active = True
        self.user.save()
        super().setUp()





class LoginViewTest(BaseTestCase):

    def test_login_view_returns_status_OK(self):
        response = Client().get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_expected_template(self):
        response = Client().get(reverse('users:login'))
        self.assertTemplateUsed(response, conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['login'])

    def test_success_page_displays_expected_message(self):
        data = {'username': self.email, 'password': self.password}
        response = Client().post(reverse('users:login'), data, follow=True)
        self.assertContains(response, f'Welcome back {self.email}! You are logged in!')