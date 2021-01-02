'''
- MyAbstractUserManager instance belongs to the object attribute of the custom user class
- technically these are custom user model tests but we are specifically testing the manager methods
'''

from django.test import TestCase, Client




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()



class MyManagerTest(BaseTestCase):

    def test_manager_does_what_is_expected(self):
        pass

    