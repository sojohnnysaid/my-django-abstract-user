from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()



class MyAbstractUserTest(BaseTestCase):

    def test_str_of_user_object_is_email(self):
        my_abstract_user_instance = get_user_model().objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertEqual(str(my_abstract_user_instance), my_abstract_user_instance.email)

    def test_created_user_has_no_permissions(self):
        user_instance = get_user_model().objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        user_permissions = user_instance.get_user_permissions()
        self.assertSetEqual(user_permissions, set())

    def test_created_super_user_has_all_permissions(self):
        permissions = Permission.objects.all()
        permissions_list = [perm.content_type.app_label + '.' + perm.codename for perm in permissions]
        user_instance = get_user_model().objects.create_superuser(email='test@gmail.com', password='pP@assw0rd')
        user_permissions = list(user_instance.get_user_permissions())
        self.assertSetEqual(set(user_permissions), set(permissions_list))