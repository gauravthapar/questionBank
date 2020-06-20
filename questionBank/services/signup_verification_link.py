from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.auth.models import User
from questionBank.services import user_verification


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )


signup_verification_tokengenerator = TokenGenerator()

def generate_signup_verification_token(user):
    uidb64 = user_verification.get_uidb64_from_user(user)
    token = signup_verification_tokengenerator.make_token(user)
    return uidb64, token


def verified_user_activation(uidb64, token):
    user = user_verification.get_user_from_uidb64(uidb64)
    if user_verification.verify_signup_verification_token(uidb64, token):
        return True
    else:
        return False

