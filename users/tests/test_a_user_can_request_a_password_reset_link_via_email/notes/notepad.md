*******************************
*******
******* START 12/28/20
*******
*******************************

📜 Feature:
    ✅ A user can request to reset their password


✅ TODO LIST 
[✅] explain from users perspective
[✅] explain from framework perspective
[✅] write unit tests
[✅] pass functional test



users perspective:
    user goes to login page
    clicks forgot password link
    link takes them to password-reset-form page
    enters email
    submits form
    is redirected to login page with message 'password reset link sent to your email'


framework perspective:
    
    ✅ form:
        ✅ create form:
            ✅ email field
            ✅ use clean_email(self) method
                ✅ check if user exists. If not raise ValidationError('Email address not found in our system!')
    ✅ url name(password_reset_request): 
        ✅ create patterns:
            ✅ users/request-password-reset/

    ✅ view:
        ✅ create views:
            ✅ UsersForgotPasswordResetRequestView
                ✅ responsibilities:
                    ✅uses expected form class
                    ✅get method:
                        ✅returns expected html template
                    post method:
                        ✅calls send_password_reset_link service with expected arguments
                        ✅redirects to login page
                    
    ✅ service:
        ✅ create function signature:
            ✅ send_password_reset_link(request, user)
 
                    

*******************************
*******
******* END 12/29/20
*******
*******************************