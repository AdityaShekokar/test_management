import requests
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from test_management.settings import HOSTNAME


def create_token(user, password, client_id, client_secret):
    """
    This function is used to create authenticate user token.
    """
    data = {
        "username": user,
        "password": password,
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    token = requests.post(HOSTNAME + "o/token/", data=data)
    return {
        "access_token": token.json().get("access_token"),
        "expires_in": token.json().get("expires_in"),
        "token_type": token.json().get("token_type"),
    }


def validate_email(email):
    try:
        User.objects.get(email=email)
        raise ValidationError({"email": "unique_email_id_required"})
    except User.DoesNotExist:
        pass
