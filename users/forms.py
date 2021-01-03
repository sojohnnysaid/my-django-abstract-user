from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.urls import reverse_lazy
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe


class CustomErrorList(ErrorList):
    def __init__(self, initlist=None, error_class=None):
        super().__init__(initlist)

        if error_class is None:
            self.error_class = 'messages errorlist'
        else:
            self.error_class = 'messages errorlist {}'.format(error_class)
    
    def as_ul(self):
        if not self.data:
            return ''

        return format_html(
            '<ul class="{}">{}</ul>',
            self.error_class,
            format_html_join('', '<li class="message">{}</li>', ((e,) for e in self))
        )


class ErrorListMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = CustomErrorList


class UsersRegisterForm(ErrorListMixin, UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        return self.cleaned_data['email'].lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'confirm password'


class UsersPasswordResetRequestForm(ErrorListMixin, forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = get_user_model().objects.filter(email=email)
        if not user.exists():
            raise ValidationError('No account associated with the email you submitted!')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'email'


class UsersLoginForm(ErrorListMixin, AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if username is not None:
            user = get_user_model().objects.filter(email=username).first()

            if user is None:
                return self.get_invalid_login_error()

            if not user.is_active:
                link = reverse_lazy('users:account_activation_request')
                error_message = f"Account has not been activated! <a href={link}>Click here to resend activation link</a>"
                raise ValidationError(mark_safe(error_message))
            
        return username




class UsersAdminLoginForm(ErrorListMixin, AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if username is not None:
            user = get_user_model().objects.filter(email=username).first()

            if user is None:
                return self.get_invalid_login_error()

            if not user.is_admin:
                raise ValidationError('You are not an administrator!')
            
        return username




class UsersAccountActivationRequestForm(ErrorListMixin, forms.Form):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        user = get_user_model().objects.filter(email=email)
        if not user.exists():
            raise ValidationError('No account associated with the email you submitted!')
        return email