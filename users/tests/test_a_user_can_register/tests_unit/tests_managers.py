'''
- MyAbstractUserManager instance belongs to the object attribute of the custom user class
- technically these are custom user model tests but we are specifically testing the manager methods
'''

from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import MyAbstractUser




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()



class MyAbstractUserManagerTest(BaseTestCase):

    def test_create_user_creates_custom_user(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertIsInstance(user_instance, MyAbstractUser)

    def test_create_user_saves_email_in_all_lowercase(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='TEST@GMAIL.com', password='pP@assw0rd')
        self.assertEqual('test@gmail.com', user_instance.email)

    def test_create_user_saves_user_to_db(self):
        User = get_user_model()
        User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertEqual(len(User.objects.all()), 1)

    def test_create_user_instance_is_not_active(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertFalse(user_instance.is_active)

    def test_create_user_instance_is_not_staff(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertFalse(user_instance.is_staff)

    def test_create_user_instance_is_not_admin(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertFalse(user_instance.is_admin)

    def test_create_user_instance_is_not_super_user(self):
        User = get_user_model()
        user_instance = User.objects.create_user(email='test@gmail.com', password='pP@assw0rd')
        self.assertFalse(user_instance.is_superuser)

    def test_create_superuser_creates_custom_user(self):
        User = get_user_model()
        user_instance = User.objects.create_superuser(email='testsuper@gmail.com', password='pP@assw0rd')
        self.assertIsInstance(user_instance, MyAbstractUser)

    def test_create_superuser_saves_user_to_db(self):
        User = get_user_model()
        User.objects.create_superuser(email='testsuper@gmail.com', password='pP@assw0rd')
        self.assertEqual(len(User.objects.all()), 1)

    def test_create_superuser_instance_has_all_access_levels(self):
        User = get_user_model()
        user_instance = User.objects.create_superuser(email='test@gmail.com', password='pP@assw0rd')
        self.assertTrue(all([
            user_instance.is_active,
            user_instance.is_staff,
            user_instance.is_admin,
            user_instance.is_superuser]))