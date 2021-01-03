import re
import time

from unittest.case import skip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from django.test import LiveServerTestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
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
        self.user.is_active = False
        self.user.save()

    def tearDown(self):
        self.browser.quit()




class UserCanRequestAccountActivationLinkViaEmail(BaseFunctionalTest):
    
    
    def test_a_user_can_request_an_activation_link_when_login_error_is_account_not_activated(self):
        
        # John registers a new account
        # compelted in parent class setUp method

        # He has not had any coffee today and completely misses the message about activating his account

        # John immediately goes to the login page and trys to login
        self.browser.get(self.live_server_url + reverse('users:login'))

        # enters his email
        input = self.browser.find_elements(By.ID, 'id_username')[0]
        input.send_keys(self.email)

        # enters his password
        input = self.browser.find_elements(By.ID, 'id_password')[0]
        input.send_keys(self.password)

        # submits the form
        self.browser.find_elements(By.ID, 'users_login_form_submit_button')[0].click()

        # a message appears telling him his account is not activated
        error_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Account has not been activated!' in error_message

        # there is a link that says re-send activation link
        # he clicks the link
        self.browser.find_elements(By.LINK_TEXT, 'Click here to resend activation link')[0].click()

        # he is now on a new page 
        assert str(reverse('users:account_activation_request')) in self.browser.current_url

        # John sees a form on the page where he can enter his email
        # he enters his email
        input = self.browser.find_elements(By.ID, 'id_email')[0]
        input.send_keys(self.email)

        # he submits the form
        self.browser.find_elements(By.ID, 'users_account_activation_request_form_submit_button')[0].click()

        # John sees the page is now back to the homepage
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # There is a message that says user activation link has been re-sent! Check your email
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Form submitted. Check your email to activate your new account' in form_submitted_message

        # John has now had 3 cups of coffee and violently goes to his email
        # He sees the activation link in the email body
        email = mail.outbox[0]
        assert 'Here is your activation link' in email.subject

        # He goes to the link
        url_search = re.search(r'http://.+/account-activation/\?uid=.+&token=.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')

        # the activation link is in the email body
        activate_account_url = url_search.group(0)
        assert self.live_server_url in activate_account_url

        # He clicks the link which opens a webpage
        self.browser.get(activate_account_url)
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url
        
        # There is a success message on the page
        success_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert 'Your account has been activated! You can now login' in success_message

        # John goes to the login page
        self.browser.get(self.live_server_url + reverse('users:login'))

        # he is greeted by the login header
        assert 'Login' in self.browser.find_elements(By.TAG_NAME, 'h1')[0].text

        # John starts filling out the Login form...
        # enters his email in the username field
        input = self.browser.find_elements(By.ID, 'id_username')[0]
        input.send_keys(self.email)

        # enters his password
        input = self.browser.find_elements(By.ID, 'id_password')[0]
        input.send_keys(self.password)

        # submits the form
        self.browser.find_elements(By.ID, 'users_login_form_submit_button')[0].click()

        # he is taken to a new page
        assert str(conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']) in self.browser.current_url

        # the page tells him he is now logged in
        form_submitted_message = self.browser.find_elements(By.CLASS_NAME, 'message')[0].text
        assert f'Welcome back {self.email}! You are logged in!' in form_submitted_message
        