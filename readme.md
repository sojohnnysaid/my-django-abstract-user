# My Django AbstractUser

A Django users application you can drop into your project. It's opinionated and can be used as your CustomUser's AbstractUser to inherit from.

email is the username field

Instead of lots of templates for success pages etc, it will send
messages to a single page.

Unit tests and Functional tests were written using pytest and selenium.

Example settings.py:



## Installation

1. Drop the users folder in your project

2. Add `path('', include('users.urls')),` to your main project urls.py file

3. Add users.apps.UsersConfig to your installed apps in settings.py and add the following settings variable:
```py
from django.urls import reverse_lazy

#---- settings variables from Django
AUTH_USER_MODEL = 'users.MyAbstractUser'
LOGIN_REDIRECT_URL = reverse_lazy('users:homepage')
LOGOUT_URL = reverse_lazy('users:homepage')
#----

MY_ABSTRACT_USER_SETTINGS = {
    'users_messages_page': reverse_lazy('users:homepage'),
    'admin_messages_page':reverse_lazy('users:homepage'),
    'templates': {
        'register': 'users/register.html',
        'admin_login': 'users/admin_login.html',
        'login': 'users/login.html',
        'account_activation_request': 'users/account_activation_request.html',
        'password_reset_request': 'users/password_reset_request.html',
        'password_reset_form': 'users/password_reset_form.html',
    } 
}
```

4. To run all unit and functional tests create a pytest.ini file in the root folder with the following:
(Make sure to change the DJANGO_SETTINGS_MODULE value to your app name example: your_main_app.settings)
```
[pytest]
DJANGO_SETTINGS_MODULE = core.settings
python_files = tests.py tests_*.py *_tests.py
addopts = -x -s
; x = stops instantly on first error
```

5. pip install -r users/test_requirements.txt

6. run the command pytest to run all tests

Change the settings variable if you want to move templates to other apps, add your own user which
inherits from MyAbstractUser, or change the redirect behavior.

Hope this helps!
