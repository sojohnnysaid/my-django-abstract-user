from django.test import TestCase, Client




class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()



class MyServiceTest(BaseTestCase):

    def test_service_does_what_is_expected(self):
        pass
