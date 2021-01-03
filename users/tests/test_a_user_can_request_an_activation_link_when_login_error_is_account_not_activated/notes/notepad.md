*******************************
*******
******* START xx/xx/xx
*******
*******************************

📜 Feature:
    ✅  A user can request an activation link when login error is account not activated


✅ TODO LIST 
[✅] explain from users perspective
[] explain from framework perspective
[] write unit tests
[] pass functional test


users perspective:
    user tries to login
    a message appears on the login page:
        'This account has not been activated. Click here to resend activation link.'
    user clicks the link
    user sees a form to enter their registered username (email)
    user is redirected to the homepage with a message:
        "Account activation link has been re-sent to your registered email"
    user clicks the email link
    user is brough to the homepage with a message
        "Your account has been activated you can now login!"



framework perspective:

    [] service (re-user send_user_activation_link)

    [] form
        [] LoginForm:
            [] responsibilities:
                [] valid date user is_active status
                    [] clean_email: valid if user exists and user is not active
                    [] raise validation error:
                        [] "This account has not been activated. Click here to resend activation link.
        [] ReSendUserActivationLinkForm:
            [] responsibilities:
                [] collect user email
                    [] clean_email: valid if user exists and user is not active

    [] url name(account_activation_request):
        [] create patterns:
            [] account-activation-request
        [] view class:
            [] UsersAccountActivationRequestView

    [] view MyViewName:
        [] responsibilities:
            [] form_valid
                [] call send_user_activation_link
                [] redirect to success_url

    [] html templates
        [] create template:
            [] account_activation_request.html
                [] responsibilities:


*******************************
*******
******* END xx/xx/xx
*******
*******************************

He is on a new page account_activation_request
client get is 200 status ok