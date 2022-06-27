from ast import Return
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import datetime


def create_slug_for_task(slug_pk, user_pk):
    return force_str(urlsafe_base64_encode(force_bytes(user_pk))) + force_str(urlsafe_base64_encode(force_bytes(slug_pk)))