import string

from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token


def generate_numeric_token() -> str:
    """
    The utility function generate_numeric_token takes no parameters.
    When called, generates a string of 4 random digits. Returns the result as a string.
    """
    # return get_random_string(length=4, allowed_chars=string.digits)

    # For the purpose of testing the service on a remote service, the function has been changed to a stub
    return '1234'


def generate_referral_code() -> str:
    """
    The generate_referral_code utility function takes no parameters.
    When called, it generates a string of 6 random numbers and letters in lower and upper case.
    Returns the result as a string.
    """
    return get_random_string(length=6, allowed_chars=string.digits+string.ascii_lowercase+string.ascii_uppercase)


def send_sms_with_callback_token(user, callback_token, **kwargs) -> None:
    """
    The send_sms_with_callback_token utility function takes the following parameters,
    a user instance and a digital authentication confirmation token, as well as other named arguments.
    When called, it sends an SMS with an authentication confirmation code.

    At this stage, the function has been replaced by a stub that prints the code to the console.
    """
    print(f'На телефонный номер {user.phone} отправлен код подтверждения авторизации {callback_token}')


def create_authentication_token(user) -> Token:
    """
    The create_authentication_token utility function takes a user instance as a parameter.
    When called, it creates an instance of the Token class from the rest_framework.authtoken.models module
    to authenticate the user with the built-in user authentication system using a token.
    Returns the created instance.
    """
    return Token.objects.get_or_create(user=user)[0]
