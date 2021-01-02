from django.test import TestCase, Client




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()



class MyModelTest(BaseTestCase):

    def test_model_does_what_is_expected(self):
        pass
