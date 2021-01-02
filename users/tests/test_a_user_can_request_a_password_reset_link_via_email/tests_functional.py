import re
import time

from unittest.case import skip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from django.test import LiveServerTestCase
from django.urls import reverse
from django.core import mail
from django.conf import settings as conf_settings


class BaseFunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(15)

    def tearDown(self):
        self.browser.quit()

    def user_registers_and_activates_account(self, name):

        self.browser.get(self.live_server_url + reverse('users:register'))
        
        # enters email
        input = self.browser.find_elements(By.ID, 'id_email')[0]
        input.send_keys(f'{name}@gmail.com')

        # enters password
        input = self.browser.find_elements(By.ID, 'id_password1')[0]
        input.send_keys('p@assW00rd')

        # enters password to confirm
        input = self.browser.find_elements(By.ID, 'id_password2')[0]
        input.send_keys('p@assW00rd')

        # submits the form
        self.browser.find_elements(By.ID, 'users_register_form_submit_button')[0].click()

        # goes to email...
        email = mail.outbox[0]
        
        url_search = re.search(r'http://.+/users/account-activation/\?uid=.+&token=.+$', email.body)
        
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        activate_account_url = url_search.group(0)

        # clicks the link
        self.browser.get(activate_account_url)




class UserCanRequestPasswordResetLinkViaEmail(BaseFunctionalTest):

    
    def test_user_can_request_password_reset_link_via_email(self):

        self.user_registers_and_activates_account('John')

        # John goes to the login page
        self.browser.get(self.live_server_url + reverse('users:login'))

        # he is greeted by the login header
        assert 'Login' in self.browser.find_elements(By.TAG_NAME, 'h1')[0].text

        # John can't remember his password and notices a forgot password link
        # He clicks the link
        self.browser.find_elements(By.LINK_TEXT, 'Forgot Password? Click here!')[0].click()

        # he is taken to the password reset form page
        assert reverse('users:password_request_reset_link') in self.browser.current_url

        # he is greeted by the password reset header
        assert 'Password Reset' in self.browser.find_elements(By.TAG_NAME, 'h1')[0].text

        # he sees a form with a field to enter his email
        input = self.browser.find_elements(By.ID, 'id_email')[0]
        assert input.get_attribute('placeholder') == 'email'

        # he enters his email
        input.send_keys('john@gmail.com')

        # submits the form
        self.browser.find_elements(By.ID, 'users_password_reset_request_form_submit_button')[0].click()

        # he is taken back to the homepage
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # the page tells him an email has been sent with a confirmation link
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Success! A password reset link was sent to your email.' in form_submitted_message

