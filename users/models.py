from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.utils import generate_numeric_token, generate_referral_code


class MyUserManager(BaseUserManager):
    """
    The MyUserManager class inherits from the BaseUserManager class from the django.contrib.auth.base_user module
    and overrides its functionality for the correct functioning of the application.
    """
    use_in_migrations = True

    def create_user(self, phone: str, **extra_fields):
        """
        The create_user function overrides the base class method.
        Gets or creates a user object if it does not exist in the database.
        Returns a user object.
        """
        if not phone:
            raise ValueError('The given phone must be set')

        user = User.objects.get_or_create(phone=phone)

        if user.referral_code is None:
            user.referral_code = generate_referral_code()
            user.save()

        token = CallbackToken.objects.create(user=user)
        token.save()

        return user

    def create_superuser(self, phone, **extra_fields):

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(phone, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractUser):
    """
    The User class inherits from the AbstractUser class from the django.contrib.auth.models module.
    Represents the data model of the user object. Redefines the fields and logic of actions of the base model.
    """
    username = None
    password = None
    phone = PhoneNumberField(unique=True)
    referral_code = models.CharField(max_length=6, null=True, default=None)
    else_referral_code = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, default=None)
    is_verified = models.BooleanField(('verified'), default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self) -> str:
        return str(self.phone)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class CallbackToken(models.Model):
    """
    The CallbackToken class inherits from the Model base class from the django.db.models module.
    Represents the data model of an authorization confirmation token. Defines fields and limits for those fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    key = models.CharField(default=generate_numeric_token(), max_length=4)

    class Meta:
        verbose_name = 'Callback Token'
        ordering = ['-id']

    def __str__(self):
        return str(self.key)
