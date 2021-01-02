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




class UserCanRegisterTest(BaseFunctionalTest):
    
    def test_John_can_register(self):

        # John goes to the registration page
        self.browser.get(self.live_server_url + reverse('users:register'))

        # he is greeted by the registration header
        assert 'Register' in self.browser.find_elements(By.TAG_NAME, 'h1')[0].text

        # John starts filling out the registration form...

        # enters his email
        input = self.browser.find_elements(By.ID, 'id_email')[0]
        assert input.get_attribute('placeholder') == 'email'
        input.send_keys('john@gmail.com')

        # enters his password
        input = self.browser.find_elements(By.ID, 'id_password1')[0]
        assert input.get_attribute('placeholder') == 'password'
        input.send_keys('p@assW00rd')

        # enters his password to confirm
        input = self.browser.find_elements(By.ID, 'id_password2')[0]
        assert input.get_attribute('placeholder') == 'confirm password'
        input.send_keys('p@assW00rd')

        # submits the form
        self.browser.find_elements(By.ID, 'users_register_form_submit_button')[0].click()

        # he is taken to a new page
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # the page tells him an email has been sent with a confirmation link
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Form submitted. Check your email to activate your new account' in form_submitted_message

        # John goes to his email...
        email = mail.outbox[0]
        assert 'Here is your activation link' in email.subject
        
        url_search = re.search(r'http://.+/users/account-activation/\?uid=.+&token=.+$', email.body)
        
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        # the activation link is in the email body
        activate_account_url = url_search.group(0)
        assert self.live_server_url in activate_account_url