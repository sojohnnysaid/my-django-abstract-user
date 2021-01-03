import re
import time

from unittest.case import skip
from django.contrib.auth import get_user_model

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from django.test import LiveServerTestCase
from django.urls import reverse
from django.conf import settings as conf_settings


class BaseFunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(15)

        self.email = 'john@gmail.com'
        self.password = 'pP@assW0rd'
        self.user = get_user_model().objects.create_user(email=self.email, password=self.password)
        self.user.is_active = True
        self.user.is_admin = True
        self.user.save()

    def tearDown(self):
        self.browser.quit()




class UserCanLogin(BaseFunctionalTest):
    
    def test_John_the_admin_can_login(self):

        # John goes to the admin-login page
        self.browser.get(self.live_server_url + reverse('users:admin_login'))

        # he is greeted by the admin-login header
        assert 'Admin Login Page' in self.browser.find_elements(By.TAG_NAME, 'h1')[0].text

        # John starts filling out the admin-login form...

        # enters his email in the username field
        input = self.browser.find_elements(By.ID, 'id_username')[0]
        input.send_keys(self.email)

        # enters his password
        input = self.browser.find_elements(By.ID, 'id_password')[0]
        input.send_keys(self.password)

        # submits the form
        self.browser.find_elements(By.ID, 'users_admin_login_form_submit_button')[0].click()

        # he is taken to a new page
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # the page tells him he is now logged in
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert f'Welcome back {self.email}! You are logged in! You are an admin!' in form_submitted_message