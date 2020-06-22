from questionBank.services.user_verification import generate_signup_verification_link
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_email_verification_link(request, user):
    try:
        link = generate_signup_verification_link(request, user)
        email = user.email
        message = render_to_string('questionBank/account_verification.html',{
            'user':user,
            'link':link,
        })
        email = EmailMessage(
            'Verify your email',
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = False
        email.send()
        print(message)
        return True
    except:
        return False


def feedback_reply_email(user):
    template = render_to_string('questionBank/feedback_template.html',{'name':user.student.name})
    email = EmailMessage(
        'Thanks for your feedback',
        template,
        settings.EMAIL_HOST_USER,
        [user.email],
    )
    email.fail_silently =False
    email.send()
    