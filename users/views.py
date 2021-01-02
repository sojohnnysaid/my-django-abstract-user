from django.contrib.auth.views import PasswordResetConfirmView, LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth import logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from users import forms, services

from django.conf import settings as conf_settings


# Create your views here.
class UsersRegisterView(CreateView):
    model = get_user_model()
    form_class = forms.UsersRegisterForm
    template_name = conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['register']
    success_url = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']

    def form_valid(self, form):
        self.object = form.save()
        services.send_user_activation_link(self.request, self.object)
        return HttpResponseRedirect(self.get_success_url())




class UsersAccountActivationView(RedirectView):
    url = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']
    def get(self, request, *args, **kwargs):
        services.activate_user(request)
        return super().get(request, *args, **kwargs)




class UsersLoginView(LoginView):
    template_name = conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['login']

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back {form.user_cache.email}! You are logged in!')
        return super().form_valid(form)


class UsersLogoutView(LogoutView):
    next_page = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        auth_logout(request)
        next_page = self.get_next_page()
        if next_page:
            # Redirect to this page until the session has been cleared.
            messages.success(self.request, 'You are logged out!')
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)



class UsersPasswordResetRequestView(FormView):
    template_name = conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['password_reset_request']
    form_class = forms.UsersPasswordResetRequestForm
    success_url = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']

    def form_valid(self, form):
        user = get_user_model().objects.get(email=form.cleaned_data['email'])
        services.send_password_reset_link(self.request, user)
        return HttpResponseRedirect(self.success_url)




INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
class UsersPasswordResetView(PasswordResetConfirmView):
    template_name = conf_settings.MY_ABSTRACT_USER_SETTINGS['templates']['password_reset_form']
    success_url = conf_settings.MY_ABSTRACT_USER_SETTINGS['users_messages_page']

    def form_valid(self, form):
        form.full_clean()
        form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        messages.success(self.request, 'Success! Your password has been reset.')
        # log user in and out to invalidate token after password reset form submitted
        login(self.request, form.user)
        logout(self.request)
        return HttpResponseRedirect(self.success_url)