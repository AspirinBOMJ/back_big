from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailActivatedTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        return str(user.pk) + str(timestamp) + str(user.email_active)

email_activation_token = EmailActivatedTokenGenerator()


class ResetPasswordActivatedTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        return str(user.pk) + str(timestamp) + str(user.password)

reset_password_activation_token = EmailActivatedTokenGenerator()