import re
import time

from unittest.case import skip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
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
        self.user.save()

    def tearDown(self):
        self.browser.quit()

    def user_submits_reset_password_form(self):
        #goes to the login page
        self.browser.get(self.live_server_url + reverse('users:login'))

        # can't remember password and notices a forgot password link
        # He clicks the link
        self.browser.find_elements(By.LINK_TEXT, 'Forgot Password? Click here!')[0].click()

        # he sees a form with a field to enter his email
        input = self.browser.find_elements(By.ID, 'id_email')[0]

        # he enters his email
        input.send_keys(self.email)

        # submits the form
        self.browser.find_elements(By.ID, 'users_password_reset_request_form_submit_button')[0].click()
        




class UserCanResetTheirPasswordUsingEmailedLinkOnce(BaseFunctionalTest):

    
    def test_user_can_reset_password_using_emailed_link_once(self):
        
        self.user_submits_reset_password_form() # mail.outbox[0] will hold account activation email

        # John goes to his email...
        email = mail.outbox[0]
        assert 'Here is your password reset link' in email.subject
        
        url_search = re.search(r'http://.+/password-reset/.+/.+$', email.body)
        
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        # the activation link is in the email body
        password_reset_url = url_search.group(0)
        assert self.live_server_url in password_reset_url

        # He clicks the link
        self.browser.get(password_reset_url)
        
        # John is taken to a password reset form page
        assert '/password-reset/' in self.browser.current_url

        # He enters his password in the first password field
        new_password = 'mynewPp@assW0rd'
        input = self.browser.find_elements(By.NAME, 'new_password1')[0]
        input.send_keys(new_password)
    
        # He re-enters his password in the confirm password field
        input = self.browser.find_elements(By.NAME, 'new_password2')[0]
        input.send_keys(new_password)

        # finally he submits the form
        self.browser.find_elements(By.ID, 'users_password_reset_form_submit_button')[0].click()

        # the page reloads and John notices he is now on another page
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # there is a message on the page letting him know his password was reset successfully
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Success! Your password has been reset.' in form_submitted_message