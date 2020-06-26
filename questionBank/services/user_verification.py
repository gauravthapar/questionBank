from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from questionBank.services.signup_verification_link import generate_signup_verification_token, signup_verification_tokengenerator

def get_user_from_uidb64(uidb64):
    user_id = force_bytes(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, id=user_id)
    return user

def get_uidb64_from_user(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    return uidb64

def generate_signup_verification_link(request, user):
    uidb64, token = generate_signup_verification_token(user)
    current_site = get_current_site(request)
    domain = current_site.domain
    link = f'http://{domain}/verify/{uidb64}/{token}'
    return link

def verify_signup_verification_token(uidb64, token):
    try:
        user = get_user_from_uidb64(uidb64)
    except(TypeError, ValueError, OverflowError, User.DoesNotExists):
        user = None
    if user is not None and signup_verification_tokengenerator.check_token(user, token):
        return True
    else:
        return False