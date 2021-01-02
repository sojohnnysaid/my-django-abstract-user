from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UsersRegisterForm(UserCreationForm):

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




class UsersPasswordResetRequestForm(forms.Form):
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