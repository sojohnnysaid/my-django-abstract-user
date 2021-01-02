import re
import time

from unittest.case import skip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from django.test import LiveServerTestCase
from django.urls import reverse


class BaseFunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(15)

    def tearDown(self):
        self.browser.quit()




class MyFunctionalTest(BaseFunctionalTest):
    
    def test_a_story_from_the_user_perspective(self):
        
        # John registers a new account

        # He has not had any coffee today and completely misses the message about activating his account

        # John immediately goes to the login page and trys to login

        # a message appears telling him his account is not activated

        # these is a link that says re-send activation link

        # he clicks the link

        # he sees a form on the page where he can enter his email

        # he enters his email

        # he submits the form

        # John sees the page is now back to the homepage

        # There is a message that says user activation link has been re-sent! Check your email

        # John has now had 3 cups of coffee and violently goes to his email

        # He sees the activation link in the email body

        # He goes to the link

        # The webpage is now back on the login page

        # There is a message that says the account has been activated

        # John logs in

        # He is greeted to a welcome message on the homepage letting him know he has logged in successfully
        pass