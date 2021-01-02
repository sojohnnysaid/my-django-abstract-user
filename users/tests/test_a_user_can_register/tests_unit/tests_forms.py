from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users import forms, models





class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class UsersRegisterFormTest(BaseTestCase):

    def test_uses_MyAbstractUser_model(self):
        form = forms.UsersRegisterForm
        self.assertEqual(form._meta.model, models.MyAbstractUser)

    def test_renders_correct_fields(self):
        form = forms.UsersRegisterForm
        field_names = list(form.base_fields.keys())
        self.assertEqual(['email', 'first_name', 'password1', 'password2'], field_names)

    def test_fields_use_placeholder_attributes(self):
        response = self.client.get(reverse('users:register'))
        self.assertIn('placeholder="first name"', response.rendered_content)
        self.assertIn('placeholder="email"', response.rendered_content)