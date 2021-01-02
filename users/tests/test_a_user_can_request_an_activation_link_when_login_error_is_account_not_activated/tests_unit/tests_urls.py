from unittest import skip
from django.test import TestCase
from django.urls import reverse, resolve

from users import views


class BaseTestCase(TestCase):

    def setUp(self):
        super().setUp()




class YourUrlTest(BaseTestCase):

    @skip
    def test_calls_correct_view(self):
        expected_class = views.YourView
        name = ''
        resolver_match = resolve(reverse(name))
        resolved_class = resolver_match.func.view_class
        self.assertEqual(expected_class, resolved_class)