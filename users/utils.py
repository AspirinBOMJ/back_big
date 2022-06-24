from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class EmailActivatedTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int):
        pass