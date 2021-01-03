from django.test import TestCase, Client




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class MyFormTest(BaseTestCase):

    def test_form_does_what_is_expected(self):
        pass