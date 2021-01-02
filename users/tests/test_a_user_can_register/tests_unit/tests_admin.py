from django.test import TestCase
from django.contrib import admin as django_admin

from users import admin, models

class AdminTests(TestCase):

    def test_UserCreationForm_uses_MyAbstractUser(self):
        assert admin.UserCreationForm()._meta.__dict__['model'] == models.MyAbstractUser

    def test_UserChangeForm_uses_MyAbstractUser(self):
        assert admin.UserChangeForm()._meta.__dict__['model'] == models.MyAbstractUser

    def test_UserAdmin_uses_Custom_Forms(self):
        assert admin.UserAdmin.__dict__['form'] == admin.UserChangeForm
        assert admin.UserAdmin.__dict__['add_form'] == admin.UserCreationForm

    def test_custom_admin_registered(self):
        registry = django_admin.site._registry
        assert models.MyAbstractUser in registry
        self.assertIsInstance(registry[models.MyAbstractUser], admin.UserAdmin)