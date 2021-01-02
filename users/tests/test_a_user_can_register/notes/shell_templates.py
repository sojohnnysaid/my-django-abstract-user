#------------------#
# Test User exists #
#------------------#
from django.contrib.auth import get_user_model
all_users = get_user_model().objects.all()
user = get_user_model().objects.filter(email='john@gmail.com').exists()



#-------------------------#
# Test Client get request #
#-------------------------#
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from random import randrange

# create a user
random_number = randrange(100000)
email = f'{random_number}John@gmail.com'
password = 'pPa@ssw0rd'
user = get_user_model().objects.create_user(email=email, password=password)

c = Client()
name = 'users:password_request_reset_link'
response = c.get(reverse(name))




#-------------------------#
# Test Client post request #
#-------------------------#
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from random import randrange

# create a user
random_number = randrange(100000)
email = f'{random_number}John@gmail.com'
password = 'pPa@ssw0rd'
user = get_user_model().objects.create_user(email=email, password=password)

c = Client()
name = 'users:password_request_reset_link'
data = {'email': 'wrong@gmail.com'}
response = c.post(reverse(name), data)




#-------------#
# Test a Form #
#-------------#
from django.contrib.auth import get_user_model

from random import randrange

from users import forms

# create a user
random_number = randrange(100000)
email = f'{random_number}John@gmail.com'
password = 'pPa@ssw0rd'
user = get_user_model().objects.create_user(email=email, password=password)

# create form object
blank_form = forms.UsersPasswordResetRequestForm()
form = forms.UsersPasswordResetRequestForm({'email': f'{random_number}JOHN@GMAIL.com'})




#-------------------#
# Test a view class #
#-------------------#
from django.test import RequestFactory
from django.urls import reverse
from users import views

request = RequestFactory().get(reverse('users:password_request_reset_link'))
response = views.UsersPasswordResetRequestView.as_view()(request)
response.template_name[0]




#---------------------------#
# Test Password Reset Token #
#---------------------------#
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.test import Client

from random import randrange

# create a user
email = f'{randrange(100000)}test_password_reset@gmail.com'
password = 'pPa@ssw0rd'
user = get_user_model().objects.create_user(email=email, password=password)

# generate a password reset token
token = default_token_generator.make_token(user)

# check if token is valid
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)

# login the user
client = Client()
client.force_login(user)

# check if token is still valid
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)
default_token_generator.check_token(user, token)