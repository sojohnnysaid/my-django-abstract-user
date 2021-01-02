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


    def submit_register_user_form(self, name):
        
        self.browser.get(self.live_server_url + reverse('users:register'))
        
        # enters email
        input = self.browser.find_elements(By.ID, 'id_email')[0]
        input.send_keys(f'{name}@gmail.com')
        
        # enters first name
        input = self.browser.find_elements(By.ID, 'id_first_name')[0]
        input.send_keys(f'{name}')

        # enters password
        input = self.browser.find_elements(By.ID, 'id_password1')[0]
        input.send_keys('p@assW00rd')

        # enters password to confirm
        input = self.browser.find_elements(By.ID, 'id_password2')[0]
        input.send_keys('p@assW00rd')

        # submits the form
        self.browser.find_elements(By.ID, 'users_register_form_submit_button')[0].click()




class UserCanActivateAccountUsingLinkOnceTest(BaseFunctionalTest):
    
    def test_John_can_activate_account_using_link_once(self):
        
        self.submit_register_user_form('John')

        # John goes to his email...
        email = mail.outbox[0]
        assert 'Here is your activation link' in email.subject

        url_search = re.search(r'http://.+/users/account-activation/\?uid=.+&token=.+$', email.body)

        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        activate_account_url = url_search.group(0)
        assert self.live_server_url in activate_account_url

        # and clicks the link
        self.browser.get(activate_account_url)
        
        # John is taken to the home page
        assert str(conf_settings.USERS_ACTIVATE_USER_ACCOUNT_SUCCESS_URL) in self.browser.current_url
        navbar = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Your account has been activated! You can now login' in navbar