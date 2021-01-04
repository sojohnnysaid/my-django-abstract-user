# My Django AbstractUser

A Django users application you can drop into your project. It's opinionated and can be used as your CustomUser's AbstractUser to inherit from.

email is the username field

Instead of lots of templates for success pages etc, it will send
messages to a single page.

Unit tests and Functional tests were written using pytest and selenium.

Example settings.py:

```py
#---- settings variables from Django
AUTH_USER_MODEL = 'users.YourCustomUser'
LOGIN_REDIRECT_URL = reverse_lazy('app:url_name')
LOGOUT_URL = reverse_lazy('app:url_name')
#----

MY_ABSTRACT_USER_SETTINGS = {
    'users_messages_page': reverse_lazy('app:url_name'),
    'admin_messages_page':reverse_lazy('app:url_name'),
    'templates': {
        'register': 'app/template.html',
        'admin_login': 'app/template.html',
        'account_activation_request': 'app/template.html',
        'login': 'app/template.html',
        'password_reset_request': 'app/template.html',
        'password_reset_form': 'app/template.html',
    } 
}
```

When I drop this into my projects it's helpful to look at the tests, however I usually delete them once I start
adding fields to my app's custom user model, and start writting my own tests specific to the app i'm working on.
