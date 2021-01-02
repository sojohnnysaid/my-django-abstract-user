from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users import forms, models



class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()

        email = 'john@gmail.com'
        password = 'pP@assW0rd'
        get_user_model().objects.create_user(email=email, password=password)




class UsersPasswordResetRequestFormTest(BaseTestCase):

    def test_renders_expected_instance(self):
        form = forms.UsersPasswordResetRequestForm()
        self.assertIsInstance(form, forms.UsersPasswordResetRequestForm)


    def test_has_correct_fields(self):
        form = forms.UsersPasswordResetRequestForm()
        self.assertEqual(list(form.fields.keys()), ['email'])


    def test_form_converts_email_to_lowercase(self): 
        form = forms.UsersPasswordResetRequestForm({'email': 'JOHN@GMAIL.com'})
        form.cleaned_data = {'email':'JOHN@GMAIL.com'}
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'john@gmail.com')


    def test_form_email_field_raises_validation_error_when_user_not_found(self):
        self.assertFalse(get_user_model().objects.filter(email='wrong@gmail.com').exists())
        form = forms.UsersPasswordResetRequestForm({'email': 'wrong@gmail.com'})
        self.assertEqual(form.errors['email'], ['No account associated with the email you submitted!'])
        