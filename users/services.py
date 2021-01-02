from django.core.mail import send_mail
from django.urls.base import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator as default_password_reset_token_generator


from users.tokens import default_account_activation_token_generator as activate_user_token_generator

def get_activation_link(request, user):
        token = activate_user_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        absolute_uri = request.build_absolute_uri(reverse_lazy('users:account_activation'))
        return f'{absolute_uri}?uid={uid}&token={token}'


def send_user_activation_link(request, user):
    email_subject = 'Here is your activation link'
    email_body = get_activation_link(request,user)
    email_from = 'noreply@example.com'
    email_to = [user.email]

    send_mail(
        email_subject,
        email_body,
        email_from,
        email_to,
        fail_silently=False,
    )
    return messages.success(request, 'Form submitted. Check your email to activate your new account')


def activate_user(request):
    token = request.GET.get('token')
    user_pk = urlsafe_base64_decode(request.GET.get('uid')).decode('utf-8')
    user = get_user_model().objects.get(pk=user_pk)

    if not activate_user_token_generator.check_token(user, token):
        return messages.error(request, "sorry this token is no longer valid!")
    
    user.is_active = True
    user.save()
    return messages.success(request, 'Your account has been activated! You can now login!')


def get_password_reset_link(request, user):
        token = default_password_reset_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        absolute_uri = request.build_absolute_uri(
            reverse_lazy(
                'users:password-reset',
                kwargs={'uidb64': uid, 'token': token}))
        return absolute_uri


def send_password_reset_link(request, user):
    email_subject = 'Here is your password reset link'
    email_body = get_password_reset_link(request, user)
    email_from = 'noreply@example.com'
    email_to = [user.email]

    send_mail(
        email_subject,
        email_body,
        email_from,
        email_to,
        fail_silently=False,
    )
    return messages.success(request, 'Success! A password reset link was sent to your email.')